from fastapi import FastAPI,Path 
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
students ={
    1:{
        "name": "Ashmit Amit Rane",
        "age": "13 years old",
        "year": "8th standard",
        "hobbies": "Playing Roblox:Grow a garden, and irritating his brother"
    },
    2:{
        "name": "Bharvi Abhijeet Mali",
        "age": "9 years old",
        "year": "3rd standard",
        "hobbies": "Watching unicorns and kicking Ashmit"
    },
    3:{
        "name": "Vedang Vishal Raul",
        "age": "19 years old",
        "year": "Third year degree college",
        "hobbies": "Playing games and sleeping"
    }
}
class Student(BaseModel): #Using Basemodel to create a schema for the student data 
    name: str
    age: str
    year: str
    hobbies: str
class updatestudent(BaseModel):    #This is a schema used to update a students info.
    name: Optional[str] = None #The Optional[str]= None is used to ensure that user can edit a single value instead of all values for it to work.
    age: Optional[str] = None
    year: Optional[str] = None
    hobbies: Optional[str] = None

@app.get("/") # This is the default page of the api
def index():
    return {"message": "Newsly backend is FUCKING live!"}
@app.get("/login") # An endpoint for login
def login():
    return {"message": "You have succesfully arrived at the FUCKING login page!"}
@app.get("/student_desc/{std_id}") # This endpoint will take a student ID and return the student's description from the dictionary created above named students 
def std_info(std_id: int):
    if std_id in students:

        return{"message":"Welcome to student description page !\n","Description":students[std_id]}
    else:
        return{"message":"Invalid ID"}
@app.get("/get_by_name")# This is an example of using a query parameter to get student information by name
def std_name(name: Optional[str] = None):#BY using optional we can make the name parater in docs optional it neccesaary to put 'None' to ensure that it can accept blank values,
                                         #This us done by using the Path and Optional from fastapi
    for std_id in students:
        if students[std_id]["name"] == name:
            return students[std_id]
    return{"Data":"Not found."}
@app.post("/create_std/{std_id}") #This uses the class defined above to create a new student entry in the students dictionary, Note that the key created by this endpoint is not added in the main file.
                                  #It is limited to the docs webpage only.
def create_std(std_id : int, student : Student): #student is a variable which will refer to Student class.
    if std_id in students:
        return {"message":"The student already exists."}  
    for existing_std in students.values():
        if(
            existing_std["name"] == student.name #By using this we can avoid duplicate entirs into the database.
        ):
            return{"mesaage":"This name is already associated with a different ID"}
    students[std_id]= student
    return students[std_id]  
@app.put("/update-student/{std_id}")
def updating(student: updatestudent, std_id: int):
    if std_id not in students:
        return {"Error": "Student is not in the list"}
    
    if student.name is not None:
        students[std_id].name = student.name
    if student.age is not None:
        students[std_id].age = student.age
    if student.year is not None:
        students[std_id].year = student.year
    if student.hobbies is not None:
        students[std_id].hobbies = student.hobbies

    return students[std_id]
@app.delete("/delete_student/{std_id}")
def deleting(std_id: int):
    if std_id not in students:
        return{"Mesaage": "Student does not exists in this database."}
    del students[std_id]
    return {"Message": "Student data deleted successfully."}

