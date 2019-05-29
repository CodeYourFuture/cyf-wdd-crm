import psycopg2
import uuid

USERNAME = 'seykuyinu@gmail.com'
PASSWORD = 'CYFvolunteer19'


def insert_new_volunteer(volunteer_data):
    name = volunteer_data.get('name')
    surname = volunteer_data.get('surname')
    cyf_city = volunteer_data.get('cyfCity')
    email = volunteer_data.get('email')
    phone_number = volunteer_data.get('contactNumber')
    experience = volunteer_data.get('generalExperience')
    weekend_availability = volunteer_data.get('weekendAvailability')
    current_volunteer = volunteer_data.get('currentlyVolunteering')
    technical_skills = volunteer_data.get('technicalSkills')
    userID = uuid.uuid1()

    db_user = "something"
    db_password = "something"

    conn = psycopg2.connect(host="cyf-wdd-volunteers.cispm8rjoafp.eu-west-2.rds.amazonaws.com",
                            database="cyf_volunteers",port="8080",user=db_user, password=db_password)

    query_userID = " SELECT user_id" \
                   " FROM volunteer_info"

    session = conn.cursor()

    session.execute(query_userID)

    sql_info = "INSERT into volunteer_info " \
               "VALUES('%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', '%s')" % \
               (userID, name, surname, cyf_city, email, phone_number, experience, weekend_availability,
                current_volunteer)

    session.execute(sql_info)
    conn.commit()

    for skill in technical_skills:
        skill_type = skill.get('skillType')
        level = skill.get('level')

        sql_tech = "INSERT into volunteer_technical_skill " \
                "VALUES('%s', '%s', %d)" % \
                    (userID, skill_type, level)

        session.execute(sql_tech)
        conn.commit()

    session.close()
    conn.close()


def check_user_exist(db_users, user_id):
    """
        Checks if the user_id already exist:
    """
    check = db_users[db_users['USER_ID'].str.contains(user_id)]

    if check.count() == 0:
        return False
    elif check.count()> 0:
        return True


def get_parameter_value(param_name, decryption=False):
    param_store_client = boto3.client('ssm')
    response = param_store_client.get_parameter(
        Name=param_name,
        WithDecryption=decryption
    )

    param_value = response['Parameter']['Value']

    return param_value


def fetch_volunteers(volunteer_filter):
    # Untested function
    conn = psycopg2.connect(host="cyf-wdd-volunteers.cispm8rjoafp.eu-west-2.rds.amazonaws.com",
                            database="cyf_volunteers", port="8080", user=USERNAME, password=PASSWORD)

    cursor = conn.cursor()
    # query = "SELECT * FROM volunteer_info"
    sql_filter = ' AND '.join(['{0} LIKE \'%{1}%\''.format(k, v) for k, v in volunteer_filter.items()])
    query = """
        SELECT * FROM volunteer_info
        WHERE {};
    """.format(sql_filter)
    cursor.execute(query)
    return cursor.fetchall()
