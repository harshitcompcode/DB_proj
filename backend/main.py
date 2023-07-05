from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Create the FastAPI app
app = FastAPI()

# Configure the database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rebootl5@localhost/postgres"  # Replace with your PostgreSQL connection details
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Define the table model with a different table name
class MyData(Base):
    __tablename__ = "my_data"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(String)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    open = Column(Float)
    volume = Column(Float)
    instrument = Column(String)


# Create the table
Base.metadata.create_all(bind=engine)


# API endpoint to handle CSV upload and save data to the database
@app.post("/upload-data/")
async def upload_data(file: UploadFile = File(...)):
    db = SessionLocal()

    # Read the uploaded CSV file
    content = await file.read()
    df = pd.read_csv(content)

    # Parse and insert data into the database
    for _, row in df.iterrows():
        data = MyData(
            datetime=row["datetime"],
            close=row["close"],
            high=row["high"],
            low=row["low"],
            open=row["open"],
            volume=row["volume"],
            instrument=row["instrument"],
        )
        db.add(data)

    db.commit()
    db.close()

    return JSONResponse(content={"message": "Data uploaded successfully"})


# API endpoint to fetch data from the database
@app.get("/get-data/")
async def get_data():
    db = SessionLocal()

    # Fetch data from the table
    data = db.query(MyData.volume, MyData.instrument).all()

    # Prepare the response as a list of dictionaries
    response = [{"volume": d.volume, "instrument": d.instrument} for d in data]

    db.close()

    return JSONResponse(content=response)
