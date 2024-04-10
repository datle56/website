import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, update, insert
from fastapi.staticfiles import StaticFiles
from bs4 import BeautifulSoup
from fastapi.responses import FileResponse  # Thêm dòng này

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templatess/")

# Create a new engine instance
engine = create_engine('sqlite:///./views.db')

metadata = MetaData()

views = Table(
   'views', metadata, 
   Column('file_html', String), 
   Column('views', Integer),
)

metadata.create_all(engine)

# Reflect the tables
metadata.reflect(bind=engine)


# Get the "views" table
views_table = Table('views', metadata, autoload=True)

def update_views(engine, views_table, file_html):
    with engine.connect() as connection:
        query = select(views_table).where(views_table.c.file_html == file_html)
        result = connection.execute(query).fetchone()

        if result:
            new_views = result['views'] + 1
            query = update(views_table).where(views_table.c.file_html == file_html).values(views=new_views)
            connection.execute(query)
        else:
            new_views = 1
            query = insert(views_table).values(file_html=file_html, views=new_views)
            connection.execute(query)
    
    return new_views




# Định nghĩa thư mục chứa các tệp HTML
html_dir = "./templates"
titles_descriptions_filenames = []

# Iterate over each file in the directory
for filename in os.listdir(html_dir):
    # Check if the file is an HTML file
    if filename.endswith(".html"):
        # Join the directory path with the filename
        file_path = os.path.join(html_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f: 
            soup = BeautifulSoup(f.read(), 'html.parser')

            # Extract the title, description, and file name from the meta tags
            title = soup.title.string if soup.title else 'No title'
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'] if description_tag else 'No description'
            file_name = filename[:-5]  # Remove the ".html" extension

            titles_descriptions_filenames.append((title, description, file_name))

def create_route_handler(file_html):
    async def route_handler(request: Request):
        # Update the view count in the database and get the new view count
        new_views = update_views(engine, views_table, file_html)

        # Print the new view count
        print(f"The page {file_html} has been viewed {new_views} times.")

        return templates.TemplateResponse(f"{file_html}.html", {"request": request})
    
    return route_handler

# Iterate over each file in the directory
for filename in os.listdir(html_dir):
    # Check if the file is an HTML file
    if filename.endswith(".html"):
        # Get the name of the file without the extension
        file_html = filename[:-5]

        # Define a new route for each HTML file
        app.get(f"/{file_html}", response_class=HTMLResponse)(create_route_handler(file_html))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, page: int = 1):
    # Calculate the start and end indices for the titles, descriptions, and file names to display
    start = (page - 1) * 10
    end = start + 10

    # Get the titles, descriptions, and file names for the current page
    current_titles_descriptions_filenames = titles_descriptions_filenames[start:end]

    # Calculate the next and previous page numbers
    next_page = page + 1 if end < len(titles_descriptions_filenames) else None
    prev_page = page - 1 if start > 0 else None

    return templates.TemplateResponse("index.html", {"request": request, "titles_descriptions_filenames": current_titles_descriptions_filenames, "next_page": next_page, "prev_page": prev_page})


@app.get("/sitemap.xml")
async def get_sitemap():
    return FileResponse("/root/code/website/sitemap.xml", media_type="application/xml")