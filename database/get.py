mysql2 = "SELECT user_id from wp_usermeta where meta_key = 'telegramid' and meta_value = %s"
mysql3 = "SELECT user_status from wp_users where ID = %s"
mysql4 = "SELECT meta_value from wp_usermeta where meta_key = 'auth_2' and user_id = %s"
mysql5 = "SELECT user_pass from wp_users where user_login = %s;"
mysql6 = "SELECT ID from wp_users where user_login = %s"
mysql7 = "SELECT forusers from wp_democracy_q where id = %s"
mysql8 = "SELECT active from wp_democracy_q where id = %s"
mysql9 = "SELECT logid from wp_democracy_log where qid = %s and userid = %s"
mysql10 = "SELECT COUNT(id) from wp_democracy_q"
mysql11 = "SELECT question from wp_democracy_q where id = %s"
mysql12 = "SELECT id from wp_democracy_q"
mysql13 = "SELECT user_role from wp_users where ID = %s"
