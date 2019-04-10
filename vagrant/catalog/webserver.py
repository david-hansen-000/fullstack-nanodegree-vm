import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer

from database_setup import Base, Restaurant
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST'
                    enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2>
                    <input name="message" type="text" >
                    <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST'\
                    enctype='multipart/form-data' action='/hello'>\
                    <h2>What would you like me to say?</h2>\
                    <input name="message" type="text">\
                    <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<a href='/restaurants/new'>Create a new "
                output += "restaurant</a>"
                output += "<h1>Restaurant List</h1>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "{}</br>".format(restaurant.name)
                    output += "<a href='/restaurant/{}/edit'>edit</a><br>\
                    <a href='#'>delete</a><br><br>".format(restaurant.id)
                output += "</body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h3>Create a new restaurant name</h3>"
                output += "<form method = 'POST' enctype='multipart/form-data'\
                    action='/restaurants/new'>"
                output += "<input name='restaurant' type='text'>"
                output += "<input type='submit' value='submit'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/edit"):
                path = self.path
                separate = path.split("/")
                id_part = separate[2]
                e_restaurant = session.query(Restaurant).filter_by(id=id_part).one()
                print("restaurant should be set")
                print(type(e_restaurant))
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                output = "<html><body><h1>Editing {}</h1><br>".format(e_restaurant.name)
                output += "<form method = 'POST' enctype='multipart/form-data'\
                        action='/restaurants/{}/edit'>".format(id_part)
                output += "<input name='id' type='text' value='{}'\
                        size='1' readonly>".format(id_part)
                output += "<input name='restaurant' type='text' value='{}'>" \
                    .format(e_restaurant.name)
                output += "<input type='submit' value='Submit'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.get('content-type'))
                pdict['boundary'] = pdict['boundary'].encode('utf-8')
                content_len = int(self.headers.get('Content-Length'))
                pdict['CONTENT-LENGTH'] = content_len
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant')
                    new_restaurant = Restaurant(name=restaurant_name[0])
                    session.add(new_restaurant)
                    session.commit()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header( \
                    self.headers.get('content-type'))
                pdict['boundary'] = pdict['boundary'].encode('utf-8')
                content_len = int(self.headers.get('Content-Length'))
                pdict['CONTENT-LENGTH'] = content_len
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant')
                    post_id_part = fields.get('id')
                    print("we'd be changing the restaurant with id:{} to {}"
                          .format(post_id_part[0], restaurant_name[0]))
                    edit_restaurant = session.query(Restaurant)\
                        .filter_by(id=post_id_part[0]).one()
                    edit_restaurant.name = restaurant_name[0]
                    print("new set restaurant:", edit_restaurant.get())
                    session.add(edit_restaurant)
                    session.commit()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurant')
            self.end_headers()

        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            print("type:", type(edit_restaurant))
            print("repr:", repr(edit_restaurant))
            print(e)
            session.rollback()
            session.close()


def main():
    try:
        port = 8020
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        session.close()
        server.socket.close()


if __name__ == '__main__':
    main()
