import mysql
import timedelta
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'leen'

# connect the python back end with the data base

# database connection configuration

db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'astroclub'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


# gets the home page initially
@app.route('/')
def home():
    return render_template('main.html')


# admin login methods
@app.route('/AdminLogin')
def admin_login():
    print("AdminLogin route accessed")
    return render_template('admin_login.html')


@app.route('/getMembersPage')
def member_page():
    print("member route accessed")
    return render_template('members.html')


@app.route('/getEventPage')
def Event_Page():
    print("Event page route accessed")
    return render_template('Event.html')


@app.route('/getPhotoPage')
def Photo_Page():
    print("photo page route accessed")
    return render_template('image.html')


@app.route('/getResources')
def Resource_Page():
    print("Resource page route accessed")
    return render_template('Resources.html')


@app.route('/getResearches')
def Research_Page():
    print("Research page route accessed")
    return render_template('Researches.html')


# Route for handling login form submission
@app.route('/admin-dashboard', methods=['GET'])
def admin_dashboard1():
    if session.get('logged_in'):
        return render_template('admin-dashboard.html')
    else:
        return redirect(url_for('admin_login'))

    # Route for handling login form submission


@app.route('/admin-dashboard', methods=['POST'])
def admin_dashboard():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "admin" and password == "7777":
        session['logged_in'] = True
        return render_template('admin-dashboard.html')  # Redirect to dashboard
    else:
        return redirect(url_for('login'))


# for the resources page
@app.route('/links')
def links():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT resourceName,URL FROM resources")
        links = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({"links": links})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# methods for the members table

# Route to get members
@app.route('/getMembers', methods=['GET'])
def get_members():
    # Connect to the database
    try:

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()

        # Convert rows to JSON format
        data = [
            {
                'MemberID': row[0],
                'MemberName': row[1],
                'Email': row[2],
                'joinDate': row[3].strftime('%Y-%m-%d'),
                'Privilege': row[4]

            }
            for row in rows
        ]
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# delete members

@app.route('/deleteMembers', methods=['POST'])
def delete_members():
    data = request.json
    member_id = data.get('id')
    if not member_id:
        return jsonify({'message': 'Member ID is required'}), 400  # bad request
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM members WHERE MemberID=%s", (member_id,))
        connection.commit()
        rows_deleted = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_deleted > 0:
            return jsonify({'message': 'Member deleted'}), 200
        else:
            return jsonify({'message': 'Member not found'}), 404
    except Exception as error:
        print(f"Error in delete_member: {error}")  # Log the error for debugging
        return jsonify({'error': str(error)}), 500


# insert members
@app.route('/InsertMembers', methods=['POST'])
def insert_members():
    data = request.json
    member_id = data.get('id')
    member_name = data.get('name')
    email = data.get('email')
    join_date = data.get('date')
    privilege = data.get('privileges')
    if not member_id:
        return jsonify({'message': 'Member ID is required'}), 400  # Bad Request
    if not member_name:
        return jsonify({'message': 'Member name is required'}), 400  # Bad Request
    if not email:
        return jsonify({'message': 'Email is required'}), 400  # Bad Request

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO members (MemberID, MemberName, Email, joinDate, Privilege) VALUES (%s, %s, %s, %s, %s)",
            (member_id, member_name, email, join_date, privilege)
        )
        connection.commit()
        rows_inserted = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_inserted > 0:
            return jsonify({'message': 'Member inserted successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        # print(f"Error in insert_member: {error}")  # Log the error for debugging
        return jsonify({'error': str(error)}), 500

    # Search for a member by ID


@app.route('/searchMember/<int:member_id>', methods=['GET'])
def search_member(member_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM members WHERE MemberID = %s", (member_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            member = {
                'MemberID': row[0],
                'MemberName': row[1],
                'Email': row[2],
                'joinDate': row[3].strftime('%Y-%m-%d'),
                'Privilege': row[4]
            }
            return jsonify(member), 200
        else:
            return jsonify({'message': 'Member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# update the table of members

# update members
@app.route('/UpdateMembers', methods=['POST'])
def update_members():
    data = request.json

    member_id = data.get('updateMemberID')
    member_name = data.get('updateMemberName')
    email = data.get('updateEmail')
    join_date = data.get('updateJoinDate')
    privilege = data.get('updatePrivilege')
    print("test")
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE members set MemberName =%s,Email=%s,joinDate=%s,Privilege=%s where MemberID=%s ",
            (member_name, email, join_date, privilege, member_id)
        )
        connection.commit()
        rows_updated = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_updated > 0:
            return jsonify({'message': 'Member inserted successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        print(f"Error in insert_member: {error}")
    return jsonify({'error': str(error)}), 500


@app.route('/getAdminsEmails', methods=['GET'])
def get_admins_emails():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT Email FROM members WHERE Privilege like 'admin'")
        rows = cursor.fetchall()

        data = [
            {
                'Email': row['Email']
            }
            for row in rows
        ]

        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get tables for the admin page tables

@app.route('/getadminPhotos', methods=['GET'])
def get_adminPhotos():
    # Connect to the database
    try:

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM photo")
        rows = cursor.fetchall()

        # Convert rows to JSON format
        data = [
            {
                'photoID': row[0],
                'Title': row[1],
                'PhotoURL': f"static/assets/images/uploads/photo/{row[0]}.jpg",  # Construct the photo URL
                'DateTaken': row[3].strftime('%Y-%m-%d'),
                'resolution': row[4],
                'skyData': row[5],
                'TelescopeID': row[6]

            }
            for row in rows
        ]
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # get photos


@app.route('/getadminResearch', methods=['GET'])
def get_adminResearch():
    # Connect to the database
    try:

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM research")
        rows = cursor.fetchall()

        # Convert rows to JSON format
        data = [
            {
                'ResearchID': row[0],
                'Title': row[1],
                'TheSummary': row[2],
                'FileURL': row[3]

            }
            for row in rows
        ]
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/getadminResource', methods=['GET'])
def get_adminResource():
    # Connect to the database
    try:

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM resources")
        rows = cursor.fetchall()

        # Convert rows to JSON format
        data = [
            {
                'resourceID': row[0],
                'resourceName': row[1],
                'URL': row[2],

            }
            for row in rows
        ]
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/getadminTelescopes', methods=['GET'])
def get_adminTelescopes():
    # Connect to the database
    try:

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM telescopes")
        rows = cursor.fetchall()

        # Convert rows to JSON format
        data = [
            {
                'TelescopeID': row[0],
                'TheName': row[1],
                'Thecondition': row[2],

            }
            for row in rows
        ]
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/getadminEvents', methods=['GET'])
def get_adminEvents():
    # Connect to the database
    try:

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM theevents")
        rows = cursor.fetchall()

        # Convert rows to JSON format
        data = [
            {
                'EventID': row[0],
                'EventName': row[1],
                'TheDate': row[2].strftime('%Y-%m-%d'),
                'numberOFPeople': row[3],
                'location': row[4],
                'startTime': row[5].strftime('%H:%M:%S') if hasattr(row[5], 'strftime') else str(row[5]),
                'endTime': row[6].strftime('%H:%M:%S') if hasattr(row[5], 'strftime') else str(row[6]),
                'PhotoURL': row[7],
                'description': row[8],

            }
            for row in rows
        ]
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get resources
@app.route('/api/resources')
def get_resources():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT resource_name, subject, starting_date, link FROM Resources")
        resources = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(resources)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get photos
@app.route('/photosforPage')
def get_photosforPage():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM photo")
        photos = cursor.fetchall()
        for photo in photos:
            cursor.execute("SELECT TheName FROM telescopes WHERE TelescopeID = %s", (photo['TelescopeID'],))
            telescope = cursor.fetchone()
            photo['TelescopeName'] = telescope['TheName'] if telescope else None
        cursor.close()
        connection.close()
        return jsonify(photos)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/homePagePhotos')
def homepage_photos():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT Title,photoURL FROM photo")
        photos = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(photos)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# operations for photos

@app.route('/UploadPhotos', methods=['POST'])
def upload_photos():
    photo_id = request.form.get("photoID")
    photo_name = request.form.get("title")
    photo_file = request.files.get("photo")  # Access the uploaded file
    date_taken = request.form.get("dateTaken")
    resolution_forPhoto = request.form.get("resolution")
    sky_data = request.form.get("skyData")
    telescopeID = request.form.get("telescopeID")
    if photo_file:
        file_extension = photo_file.filename.split('.')[-1]
        photo_filename = f"{photo_id}.{file_extension}"
        photo_path = f"static/assets/images/uploads/photo/{photo_filename}"
        photo_file.save(photo_path)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO photo (PhotoID, Title, photoURL,DateTaken,resolution,skyData,TelescopeID) VALUES (%s,%s, %s, %s, %s, %s, %s)",
            (photo_id, photo_name, photo_path, date_taken, resolution_forPhoto, sky_data, telescopeID)
        )
        connection.commit()
        rows_inserted = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_inserted > 0:
            return jsonify({'message': 'photo inserted successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        # print(f"Error in insert_member: {error}")  # Log the error for debugging
        print(f"Error uploading photo: {error}")
        return jsonify({'error': str(error)}), 500


# delete photo

@app.route('/deletePhoto', methods=['POST'])
def delete_photo():
    data = request.json
    Photo_id = data.get('id')
    if not Photo_id:
        return jsonify({'message': 'Photo ID is required'}), 400  # bad request
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM photo WHERE photoID=%s", (Photo_id,))
        connection.commit()
        rows_deleted = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_deleted > 0:
            return jsonify({'message': 'photo deleted'}), 200
        else:
            return jsonify({'message': 'photo not found'}), 404
    except Exception as error:
        print(f"Error in delete_member: {error}")
        return jsonify({'error': str(error)}), 500


# search photos
@app.route('/searchPhoto/<int:photo_id>', methods=['GET'])
def search_photo(photo_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM photo WHERE PhotoID = %s", (photo_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            member = {
                'PhotoID': row[0],
                'Title': row[1],
                'photoURL': row[2],
                'DateTaken': row[3].strftime('%Y-%m-%d'),
                'resolution': row[4],
                'skyData': row[5],
                'TelescopeID': row[6]
            }
            return jsonify(member), 200
        else:
            return jsonify({'message': 'photo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# update the table of photos

# update photos
@app.route('/UpdatePhoto', methods=['POST'])
def update_photo():
    try:
        data = request.get_json()
        photo_id = data.get("updatePhotoID")
        photo_name = data.get("updateTitle")
        date_taken = data.get("updateDateTaken")
        resolution_forPhoto = data.get("updateResolution")
        sky_data = data.get("updateSkyData")
        telescopeID = data.get("updateTelescopeID")

        if not all([photo_id, photo_name, date_taken, resolution_forPhoto, sky_data, telescopeID]):
            return jsonify({'error': 'Missing fields'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE photo set Title =%s,DateTaken=%s,resolution=%s,skyData=%s,TelescopeID=%s where PhotoID=%s ",
            (photo_name, date_taken, resolution_forPhoto, sky_data, telescopeID, photo_id)
        )
        connection.commit()
        rows_updated = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_updated > 0:
            return jsonify({'message': 'photo updated successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        print(f"Error in update_photo: {error}")
    return jsonify({'error': str(error)}), 500


# operations for resources :

@app.route('/UploadResources', methods=['POST'])
def upload_resources():
    resource_id = request.form.get("ResourceID")
    resource_name = request.form.get("resourceName")
    resource_url = request.form.get("resourceURL")
    print(resource_id, resource_name, resource_url)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO resources (resourceID,resourceName,URL) VALUES (%s,%s, %s)",
            (resource_id, resource_name, resource_url)
        )
        connection.commit()
        rows_inserted = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_inserted > 0:
            return jsonify({'message': 'resource inserted successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        # print(f"Error in insert_member: {error}")  # Log the error for debugging
        print(f"Error uploading resource: {error}")
        return jsonify({'error': str(error)}), 500


# delete resource

@app.route('/deleteResource', methods=['POST'])
def delete_resource():
    data = request.json
    resource_id = data.get('id')
    if not resource_id:
        return jsonify({'message': 'resource ID is required'}), 400  # bad request
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM resources WHERE resourceID=%s", (resource_id,))
        connection.commit()
        rows_deleted = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_deleted > 0:
            return jsonify({'message': 'resource deleted'}), 200
        else:
            return jsonify({'message': 'resource not found'}), 404
    except Exception as error:
        print(f"Error in delete_resource: {error}")
        return jsonify({'error': str(error)}), 500


# search Resource
@app.route('/searchResource/<int:resource_id>', methods=['GET'])
def search_resource(resource_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM resources WHERE resourceID = %s", (resource_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            resource = {
                'resourceID': row[0],
                'resourceName': row[1],
                'URL': row[2]

            }
            return jsonify(resource), 200
        else:
            return jsonify({'message': 'resource not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# update the table of resources

# update resource
@app.route('/UpdateResource', methods=['POST'])
def update_resource():
    try:
        data = request.get_json()
        print("Received data:", data)
        resource_id = data.get("updateResourceID")
        resource_name = data.get("updateResourceName")
        resource_url = data.get("updateResourceURL")

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE resources set resourceName=%s,URL=%s where resourceID=%s ",
            (resource_name, resource_url, resource_id)
        )
        connection.commit()
        rows_updated = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_updated > 0:
            return jsonify({'message': 'resource updated successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        print(f"Error in update_resource: {error}")
    return jsonify({'error': str(error)}), 500


# operations for telescopes :

@app.route('/UploadTelescopes', methods=['POST'])
def upload_telescopes():
    telescope_id = request.form.get("TelescopeID")
    telescope_name = request.form.get("TheName")
    condition = request.form.get("Thecondition")

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO telescopes (TelescopeID,TheName,Thecondition) VALUES (%s,%s, %s)",
            (telescope_id, telescope_name, condition)
        )
        connection.commit()
        rows_inserted = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_inserted > 0:
            return jsonify({'message': 'telescope inserted successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        # print(f"Error in insert_member: {error}")  # Log the error for debugging
        print(f"Error uploading telescope: {error}")
        return jsonify({'error': str(error)}), 500


# delete telescope
@app.route('/deleteTelescope', methods=['POST'])
def delete_telescope():
    data = request.json
    telescope_id = data.get('id')
    if not telescope_id:
        return jsonify({'message': 'telescope ID is required'}), 400  # bad request
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM telescopes WHERE TelescopeID=%s", (telescope_id,))
        connection.commit()
        rows_deleted = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_deleted > 0:
            return jsonify({'message': 'telescope deleted'}), 200
        else:
            return jsonify({'message': 'telescope not found'}), 404
    except Exception as error:
        print(f"Error in delete_telescope: {error}")
        return jsonify({'error': str(error)}), 500


# search telescope
@app.route('/searchTelescope/<int:telescope_id>', methods=['GET'])
def search_telescope(telescope_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM telescopes WHERE TelescopeID = %s", (telescope_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            telescope = {
                'TelescopeID': row[0],
                'TheName': row[1],
                'Thecondition': row[2]

            }
            return jsonify(telescope), 200
        else:
            return jsonify({'message': 'telescope not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# update the table of telescopes

# update telescope
@app.route('/UpdateTelescope', methods=['POST'])
def update_telescope():
    try:
        data = request.get_json()
        print("Received data:", data)
        telescope_id = data.get("updateTelescopeID2")
        telescope_name = data.get("updateTelescopeName")
        telescope_condition = data.get("updateTelescopeCondition")

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE telescopes set TheName=%s,Thecondition=%s where telescopeID=%s ",
            (telescope_name, telescope_condition, telescope_id)
        )
        connection.commit()
        rows_updated = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_updated > 0:
            return jsonify({'message': 'telescope updated successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        print(f"Error in update_telescope: {error}")
    return jsonify({'error': str(error)}), 500


# operations for the research
@app.route('/UploadResearch', methods=['POST'])
def upload_research():
    print(request.form)
    research_id = request.form.get("ResearchID")
    research_name = request.form.get("Title")
    summary = request.form.get("summary")
    research_file = request.files.get("FileURL")
    date_taken = request.form.get("DateTaken")
    members = request.form.getlist("membersSelection")
    research_path = None

    print(members[0].split(','))


    print("Received member IDs:", members)
    if research_file and research_file.filename:
        file_extension = research_file.filename.split('.')[-1]
        research_filename = f"{research_id}.{file_extension}"
        research_path = f"static/assets/pdfs/{research_filename}"
        research_file.save(research_path)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()


        cursor.execute(
            "INSERT INTO research (ResearchID, Title, summary, FileURL) VALUES (%s, %s, %s, %s)",
            (research_id, research_name, summary, research_path)
        )


        for member_id in members[0].split(','):
            cursor.execute(
                "INSERT INTO member2research (MemberID, ResearchID) VALUES (%s, %s)",
                (member_id, research_id)
            )

        connection.commit()
        rows_inserted = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_inserted > 0:
            return jsonify({'message': 'Research inserted successfully'}), 200
        else:
            return jsonify({'message': 'Bad request'}), 400
    except Exception as error:
        print(f"Error uploading research: {error}")
        return jsonify({'error': str(error)}), 500


# delete research

@app.route('/deleteResearch', methods=['POST'])
def delete_research():
    data = request.json
    research_id = data.get('id')
    if not research_id:
        return jsonify({'message': 'Research ID is required'}), 400  # bad request
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM research WHERE ResearchID=%s", (research_id,))
        connection.commit()
        rows_deleted = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_deleted > 0:
            return jsonify({'message': 'research deleted'}), 200
        else:
            return jsonify({'message': 'research not found'}), 404
    except Exception as error:
        print(f"Error in delete_research: {error}")
        return jsonify({'error': str(error)}), 500


# search Research
@app.route('/searchResearch/<int:research_id>', methods=['GET'])
def search_research(research_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM research WHERE ResearchID = %s", (research_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            member = {
                'ResearchID': row[0],
                'Title': row[1],
                'summary': row[2],
                'FileURL': row[3]

            }
            return jsonify(member), 200
        else:
            return jsonify({'message': 'research not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# update the table of researches

# update research
@app.route('/UpdateResearch', methods=['POST'])
def update_research():
    try:
        data = request.get_json()
        print("Received data:", data)
        research_id = data.get("updateResearchID")
        research_name = data.get("updateTitleResearch")
        summary = data.get("updateSummary")

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE research set Title=%s,summary=%s where ResearchID=%s ",
            (research_name, summary, research_id)
        )
        connection.commit()
        rows_updated = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_updated > 0:
            return jsonify({'message': 'research updated successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        print(f"Error in update_research: {error}")
    return jsonify({'error': str(error)}), 500


# operations for events

@app.route('/UploadEvents', methods=['POST'])
def upload_events():
    event_id = request.form.get("EventID")
    event_name = request.form.get("EventName")
    date = request.form.get("TheDate")
    number_of_people = request.form.get("numberOFpeople")
    location = request.form.get("location")
    start_time = request.form.get("startTime")
    end_time = request.form.get("endTime")
    photo_file = request.files.get("PhotoURL")
    description = request.form.get("description")
    if photo_file:
        file_extension = photo_file.filename.split('.')[-1]
        photo_filename = f"{event_id}.{file_extension}"
        photo_path = f"static/assets/images/uploads/theevents/{photo_filename}"
        photo_file.save(photo_path)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO theevents (EventID, EventName, TheDate, numberOFpeople, location, startTime, endTime, PhotoURL, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (event_id, event_name, date, number_of_people, location, start_time, end_time, photo_path, description)
        )
        connection.commit()
        rows_inserted = cursor.rowcount
        cursor.close()
        connection.close()
        if rows_inserted > 0:
            return jsonify({'message': 'photo inserted successfully'}), 200
        else:
            return jsonify({'message': 'bad request'}), 400
    except Exception as error:
        # print(f"Error in insert_member: {error}")  # Log the error for debugging
        print(f"Error uploading photo: {error}")
        return jsonify({'error': str(error)}), 500


# delete events
@app.route('/deleteEvent', methods=['POST'])
def delete_event():
    data = request.json
    event_id = data.get('id')
    if not event_id:
        return jsonify({'message': 'event ID is required'}), 400  # bad request
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM theevents WHERE EventID=%s", (event_id,))
        connection.commit()
        rows_deleted = cursor.rowcount
        cursor.close()
        connection.close()

        if rows_deleted > 0:
            return jsonify({'message': 'event deleted'}), 200
        else:
            return jsonify({'message': 'event not found'}), 404
    except Exception as error:
        print(f"Error in delete_event: {error}")
        return jsonify({'error': str(error)}), 500


# search event
@app.route('/searchEvent/<int:event_id>', methods=['GET'])
def search_event(event_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM theevents WHERE EventID = %s", (event_id,))
        row = cursor.fetchone()  # Fetch one row only
        cursor.close()
        connection.close()

        if row:
            data = {
                'EventID': row[0],
                'EventName': row[1],
                'TheDate': row[2].strftime('%Y-%m-%d') if hasattr(row[2], 'strftime') else str(row[2]),
                'numberOFPeople': row[3],
                'location': row[4],
                'startTime': row[5].strftime('%H:%M:%S') if hasattr(row[5], 'strftime') else str(row[5]),
                'endTime': row[6].strftime('%H:%M:%S') if hasattr(row[6], 'strftime') else str(row[6]),
                'PhotoURL': row[7],
                'description': row[8],
            }
            return jsonify(data)
        else:
            return jsonify({'message': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# update the table of events

# update event
@app.route('/UpdateEvent', methods=['POST'])
def update_event():
    print(request.form)  # Log all form data
    print(request.files)
    event_id = request.form.get("EventID")
    event_name = request.form.get("EventName")
    date = request.form.get("TheDate")
    number_of_people = request.form.get("numberOFpeople")
    location = request.form.get("location")
    start_time = request.form.get("startTime")
    end_time = request.form.get("endTime")
    description2 = request.form.get("description")

    photo_file = request.files.get("PhotoURL")
    photo_path = None

    if photo_file and photo_file.filename:
        file_extension = photo_file.filename.split('.')[-1]
        photo_filename = f"{event_id}.{file_extension}"
        photo_path = f"static/assets/images/uploads/theevents/{photo_filename}"
        print(photo_path)
        try:
            photo_file.save(photo_path)
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({'error': 'File upload failed'}), 500
    else:

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT PhotoURL FROM theevents WHERE EventID = %s", (event_id,))
            result = cursor.fetchone()
            if result:
                photo_path = result[0]
            cursor.close()
            connection.close()
        except Exception as error:
            print(f"Error retrieving current photo URL: {error}")
            return jsonify({'error': str(error)}), 500

    try:
        query = """
            UPDATE theevents 
            SET EventName=%s, TheDate=%s, numberOFPeople=%s, location=%s, 
                startTime=%s, endTime=%s, description=%s
            WHERE EventID = %s
        """
        params = [event_name, date, number_of_people, location, start_time, end_time, description2, event_id]

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        connection.commit()
        rows_updated = cursor.rowcount
        cursor.close()
        connection.close()

        return jsonify({'message': 'Event updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    except Exception as error:
        print(f"Error in update_event: {error}")
        return jsonify({'error': str(error)}), 500


def timedelta_converter(obj):
    if isinstance(obj, timedelta):
        return str(obj)


# get events
@app.route('/events')
def get_events():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # Fetch upcoming events
        cursor.execute(
            """
           SELECT EventID, EventName, description, TheDate, startTime, endTime, photoURL, location
           FROM theevents
           WHERE TheDate >= CURDATE() ORDER BY TheDate ASC
        """)
        upcoming_events = cursor.fetchall()
        for event in upcoming_events:
            event['startTime'] = timedelta_converter(event['startTime'])
            event['endTime'] = timedelta_converter(event['endTime'])
        # Fetch past events
        cursor.execute(
            """
            SELECT EventID, EventName, description, TheDate, startTime, endTime, photoURL,location 
            FROM theevents
            WHERE TheDate<CURDATE() ORDER BY TheDate ASC
        """)
        past_events = cursor.fetchall()
        for event in past_events:
            event['startTime'] = timedelta_converter(event['startTime'])
            event['endTime'] = timedelta_converter(event['endTime'])
        cursor.close()
        connection.close()
        print("Upcoming Events:", upcoming_events)
        print("Past Events:", past_events)

        return jsonify({'upcoming': upcoming_events, 'pastEvents': past_events})

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# event timer ...
@app.route('/eventsTimer')
def get_events_timer():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""       SELECT TheDate
FROM theevents
WHERE 
 TheDate > NOW()
ORDER BY TheDate ASC
LIMIT 1;""")
        TheDate = cursor.fetchone()
        cursor.execute("""
        SELECT startTime
FROM theevents
WHERE 
 TheDate > NOW()
ORDER BY TheDate ASC
LIMIT 1;
""")
        startTimer = cursor.fetchone()
        tester = 1
        startTimer = str(startTimer['startTime'])

        TheDate = TheDate['TheDate'].strftime('%Y-%m-%d')
        print(f"TheDate: {TheDate}, startTimer: {startTimer}")
        cursor.close()
        connection.close()

        return jsonify({
            "startTimer": startTimer,
            "TheDate": TheDate,
            "tester": tester
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Research', methods=['GET'])
def research():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to get all researches
        cursor.execute("SELECT ResearchID, Title, summary, FileURL FROM research")
        researches = cursor.fetchall()

        research_data = []

        for research in researches:
            research_id = research[0]
            title = research[1]
            summary = research[2]
            file_url = research[3]

            # Get members associated with the research from member2research table
            cursor.execute("""
                SELECT m.MemberName
                FROM members m 
                JOIN member2research mr ON m.MemberID = mr.MemberID 
                WHERE mr.ResearchID = %s
            """, (research_id,))
            members = cursor.fetchall()


            member_names = [member[0] for member in members]

            research_data.append({
                'ResearchID': research_id,
                'Title': title,
                'summary': summary,
                'FileURL': file_url,
                'members': member_names
            })

        cursor.close()
        connection.close()

        return jsonify(research_data), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


#easier servers instead of using sockets etc
if __name__ == '__main__':
    app.run()
