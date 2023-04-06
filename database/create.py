mysql1 = "INSERT INTO wp_users ( user_login, user_pass, user_nicename, user_email, user_url, user_status) VALUES (%s,%s, %s, %s, %s, '0')"
mysql2 = "INSERT INTO `wp_usermeta` (user_id, meta_key, meta_value) VALUES (%s, %s, %s)"
mysql16 = "INSERT INTO wp_democracy_log (qid, aids, userid, ip_info) VALUES (%s, %s, %s, %s)"
