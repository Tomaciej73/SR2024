from deep_translator import GoogleTranslator
import mysql.connector
from config import credentials
import re
from datetime import datetime
import traceback
import requests
from decimal import Decimal, ROUND_UP, InvalidOperation, getcontext
DOMAIN_NAME = "http://karkulowskiii.com"

def save_exchange_rate_to_db(rate):
    cursor = sync_conn.cursor()
    cursor.execute("INSERT INTO exchange_rates (currency, rate) VALUES ('USD', %s)", (str(rate),))
    sync_conn.commit()

def get_exchange_rate_from_db():
    cursor = sync_conn.cursor()
    cursor.execute("SELECT rate FROM exchange_rates WHERE currency = 'USD' ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    return Decimal(result[0]) if result else None

def trans_text_pl_to_en(text: str) -> str:
    return GoogleTranslator(source="pl", target="en").translate(text)

def trans_text_en_to_pln(text: str) -> str:
    return GoogleTranslator(source="en", target="pl").translate(text)

def log_error(err_msg, err, query=None):
    print(f"{err_msg}: {err}")
    with open("error_log.txt", "a") as f:
        f.write(f"{err_msg}: {err}\n")
        if query:
            f.write(f"SQL causing error: {query}\n")
        traceback_text = ''.join(traceback.format_tb(err.__traceback__))
        f.write(f"Traceback: {traceback_text}\n")

def clean_html_tags(text):
    return re.sub(r"<[^>]*>", "", text) if text else ""

# def get_exchange_rate():
#     url = "https://api.nbp.pl/api/exchangerates/rates/a/usd/last/1/?format=json"
#     response = requests.get(url)
#     data = response.json()
#     return data['rates'][0]['mid']

def get_exchange_rate():
    rate = get_exchange_rate_from_db()
    if rate is None:
        url = "https://api.nbp.pl/api/exchangerates/rates/a/usd/last/1/?format=json"
        response = requests.get(url)
        data = response.json()
        rate = Decimal(data['rates'][0]['mid'])
        save_exchange_rate_to_db(rate)
    return rate

getcontext().prec = 6
def convert_price_to_usd(price_pln, exchange_rate):
    try:
        price_pln = Decimal(price_pln)
        exchange_rate = Decimal(exchange_rate)
        price_usd = (price_pln / exchange_rate).quantize(Decimal('1'), rounding=ROUND_UP) #Decimal('1.0')
        return price_usd
    except InvalidOperation as e:
        log_error("Convert price to USD failed", e)
        return None

# def convert_usd_to_pln(price_usd, exchange_rate):
#     try:
#         price_usd = Decimal(price_usd)
#         exchange_rate = Decimal(exchange_rate)
#         price_pln = (price_usd * exchange_rate).quantize(Decimal('1'), rounding=ROUND_UP) #Decimal('1.0')
#         return int(price_pln)
#     except InvalidOperation as e:
#         log_error("Convert USD to PLN failed", e)
#         return None

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

try:
    magento_conn = mysql.connector.connect(**credentials['magento_db'])
    presta_conn = mysql.connector.connect(**credentials['presta_db'])
    sync_conn = mysql.connector.connect(**credentials['sync_db'])

    magento_db = magento_conn.cursor()
    presta_db = presta_conn.cursor()
    sync_db = sync_conn.cursor()
    exchange_rate = get_exchange_rate()
    presta_col_list_lang = ['lang.id_product', 'lang.description', 'lang.name', 'lang.meta_title'] #ps_product_lang
    presta_col_list_shop = ['shop.price', 'shop.date_add', 'shop.date_upd'] #ps_product_shop
    query = f"""
    SELECT {', '.join(presta_col_list_lang + presta_col_list_shop)}
    FROM ps_product_lang AS lang
    JOIN ps_product_shop AS shop ON lang.id_product = shop.id_product
    WHERE 1
    """
    presta_db.execute(query)
    results = presta_db.fetchall()

    # magento_query = "SELECT value_id, value FROM catalog_product_entity_decimal"
    # magento_db.execute(magento_query)
    # results_magento = magento_db.fetchall()
    # for entity_id, price_pln in results_magento:
    #     price_usd = convert_price_to_usd(price_pln, exchange_rate)
    #     update_query_magento = "UPDATE catalog_product_entity_decimal SET value = %s WHERE value_id = %s"
    #     magento_db.execute(update_query_magento, (price_usd, entity_id))

    for row in results:
        product_id, description, name, meta_title, _, date_add, date_upd = row
        if name is None:
            continue
        name_without_html = re.sub(r"<[^>]+>", "", name)
        description_without_html = re.sub(r"<[^>]+>", "", description)

        translated_title = trans_text_en_to_pln(name_without_html)
        translated_description = trans_text_en_to_pln(description_without_html)
        presta_name_without_html = re.sub(r"<[^>]+>", "", name)

        row_without_html: tuple = tuple(
            re.sub(r"<[^>]+>", "", str(cell)) for cell in row
        )

        translated_name_pln: str = trans_text_en_to_pln(name_without_html)
        translated_description_pln: str = trans_text_en_to_pln(description_without_html)
        if name is not None:
            new_name_eng = name_without_html.replace(presta_name_without_html, translated_description_pln)
        else:
            new_name_eng = name_without_html
        presta_db.execute("SELECT price FROM ps_product_shop WHERE id_product = %s", (product_id,))
        price_pln_result = presta_db.fetchone()
        if price_pln_result is None:
            print(f"Brak ceny dla produktu {product_id}, pomijanie.")
            continue

        price_pln = price_pln_result[0]
        price_usd = convert_price_to_usd(price_pln, exchange_rate)
        if price_usd is None:
            print(f"Błąd przeliczenia ceny dla produktu {product_id}, pomijanie.")
            continue

        presta_db.execute("UPDATE ps_product_shop SET price = %s WHERE id_product = %s", (price_usd, product_id))
        presta_conn.commit()

        sync_db.execute("SELECT * FROM zadanie2 WHERE product_id = %s", (product_id,))
        existing_post = sync_db.fetchone()
        if existing_post is None:
            insert_query = "INSERT INTO zadanie2 (name, description, price, date_added, date_updated) VALUES (%s, %s, %s, %s, %s)"
            sync_db.execute(
                insert_query,
                (
                    translated_name_pln,
                    new_name_eng,
                    price_usd,
                    date_add,
                    date_upd,
                ),
            )
        else:
            update_query = """
                    UPDATE zadanie2 
                    SET name = %s, description = %s, price = %s, date_updated = %s 
                    WHERE product_id = %s
                    """
            sync_db.execute(update_query, (translated_title, translated_description, price_usd, date_upd, product_id))

        update_query_lang = """
                UPDATE ps_product_lang 
                SET description = %s, name = %s 
                WHERE id_product = %s
                """
        presta_db.execute(update_query_lang, (translated_description, translated_title, product_id))



    query_sync = f"SELECT * FROM zadanie2"
    sync_db.execute(query_sync)
    results_sync = sync_db.fetchall()
    for row in results_sync:
        sync_product_id, sync_name, sync_description, sync_price, sync_date_added, sync_date_updated = row
        try:
            sync_date_added = datetime.fromtimestamp(sync_date_added.timestamp())
            #print(f"Date Added: {sync_date_added.strftime('%Y-%m-%d %H:%M:%S')}")
        except ValueError:
            print(f"Error: sync_date_added is not a float")
        #print(f"Date Updated: {sync_date_updated.strftime('%Y-%m-%d %H:%M:%S')}")

        query_magento = """
            SELECT 
                e.entity_id,
                MAX(CASE WHEN a.attribute_id = 73 THEN v_char.value END) AS name,
                MAX(CASE WHEN a.attribute_id = 76 THEN v_text.value END) AS description,
                MAX(CASE WHEN a.attribute_id = 77 THEN v_decimal.value END) AS price,
                MAX(e.created_at) AS created_at,
                MAX(e.updated_at) AS updated_at
            FROM 
                catalog_product_entity AS e
            LEFT JOIN 
                catalog_product_entity_varchar AS v_char ON e.entity_id = v_char.entity_id AND v_char.attribute_id = 73
            LEFT JOIN 
                catalog_product_entity_text AS v_text ON e.entity_id = v_text.entity_id AND v_text.attribute_id = 76
            LEFT JOIN 
                catalog_product_entity_decimal AS v_decimal ON e.entity_id = v_decimal.entity_id AND v_decimal.attribute_id = 77
            LEFT JOIN 
                eav_attribute AS a ON a.attribute_id IN (v_char.attribute_id, v_text.attribute_id, v_decimal.attribute_id)
            GROUP BY 
                e.entity_id;
            """
        magento_db.execute(query_magento)
        results_magento = magento_db.fetchall()

        for row in results_magento:
            entity_id, magento_name, magento_description, magento_price, magento_created_at, magento_updated_at = row

            magento_name_cleaned = clean_html_tags(magento_name)
            magento_description_cleaned = clean_html_tags(magento_description)

            translated_name = trans_text_pl_to_en(magento_name_cleaned)
            translated_description = trans_text_pl_to_en(magento_description_cleaned)

            check_query = """
            SELECT COUNT(*) FROM zadanie2 
            WHERE name = %s AND description = %s AND price = %s 
            AND date_added = %s AND date_updated = %s
            """
            sync_db.execute(check_query,
                            (magento_name, magento_description, magento_price, magento_created_at, magento_updated_at))
            if sync_db.fetchone()[0] == 0:
                insert_query = """
                INSERT INTO zadanie2 (name, description, price, date_added, date_updated)
                VALUES (%s, %s, %s, %s, %s)
                """
                sync_db.execute(insert_query, (
                    translated_name, translated_description, magento_price, magento_created_at, magento_updated_at))
                print("Dodano")
            else:
                print("Istnieje.. Pomijam")
            update_query_varchar = """
                UPDATE catalog_product_entity_varchar
                SET value = %s
                WHERE attribute_id = 73 AND entity_id = %s
            """
            magento_db.execute(update_query_varchar, (translated_name, entity_id))
            update_query_text = """
                UPDATE catalog_product_entity_text
                SET value = %s
                WHERE attribute_id = 76 AND entity_id = %s
            """
            magento_db.execute(update_query_text, (translated_description, entity_id))

    sync_conn.commit()
    magento_conn.commit()
    presta_conn.commit()

except mysql.connector.IntegrityError as err:
    log_error("Wystąpił błąd integralności: ", err)
except mysql.connector.DataError as err:
    log_error("Wystąpił błąd danych: ", err)
except mysql.connector.NotSupportedError as err:
    log_error("Operacja nie jest obsługiwana: ", err)
except mysql.connector.OperationalError as err:
    log_error("Wystąpił błąd operacyjny bazy danych: ", err)
except mysql.connector.Error as err:
    log_error("Wystąpił błąd bazy danych: ", err)
except Exception as err:
    log_error("Wystąpił błąd ogólny: ", err)
finally:
    try:
        magento_conn.close()
    except mysql.connector.Error as err:
        log_error("Błąd zamykania magento_conn", err)
    try:
        presta_conn.close()
    except mysql.connector.Error as err:
        log_error("Błąd zamykania presta_conn", err)
    try:
        sync_conn.close()
    except mysql.connector.Error as err:
        log_error("Błąd zamykania sync_conn", err)
