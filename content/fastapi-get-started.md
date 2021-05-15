---
title: Get started with FastAPI
subtitle: by building polls
summary: by building polls
slug: fastapi-get-started
img: assets/img/bg.jpg
author: Andrija Jovanovic
date: 2020-05-13
---

With this blog post you'll learn how to build polls with [FastAPI](https://fastapi.tiangolo.com)


__FastAPI, What is it?__

FastAPI is a web framework for building APIs. As per its official page

> FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

It's extremely easy to learn and it is said to have speed on par with ```Node.js```.

__Installation__

To get started with FastAPI you should have two things installed:

+ FastAPI.
+ Uvicorn: the ASGI server required for FastAPI.

install them with:

+ ```pip install fastapi```
+ ```sudo pacman -S uvicorn``` or alternative for your distro.

__Basic Example__

    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def index():
        return {"message": "Welcome to the world of FastAPI!"}

    @app.get("/items/{item}")
    def read_item(item: str, q: str = None):
        return {"item": item, "q": q}
        
run the example with:

```uvicorn filename:app --reload```

where **filename** is file with code and **app** is FastAPI instance.  

open browser and go to the:  

    http://127.0.0.1:8000/
    
you should see the response:  

    
    {"message": "Welcome to the world of FastAPI!"}
    

visit:

    
    http://127.0.0.1:8000/items/apple?q=delicious
    

you should see the below response:

    {"item": "apple", "q": "delicious"}

that’s great, we have already created an API having two endpoints:

+ ```http://127.0.0.1:8000/``` doesn’t take any parameters and it simply returns a JSON response.

+ ```http://127.0.0.1:8000/items/{item}``` takes a parameter item of type str and optional str query parameter q.

another good feature of FastAPI is that it provides an interactive API documentation, simply visit:

+ ```http://127.0.0.1:8000/docs```

+ ```http://127.0.0.1:8000/redoc```.

Now let’s build our polls API. The endpoints that are created above are static, so they don’t interact with the database. In the next section we will use [SQLAlchemy](https://www.sqlalchemy.org/) for ORM and [Pydantic](https://pydantic-docs.helpmanual.io/) to create models/schemas to make our APIs dynamic.

This post assumes that you’re familiar with ```SQLAlchemy``` and that you are using Linux, you can refer this [docs](https://www.sqlalchemy.org/) for more details.

**Well make following endpoints**:

+ create poll question

+ list all poll questions

+ get question detail

+ edit poll question

+ delete poll question

+ create choice for a particular poll question

+ update votes for a particular question

**Project structure**

The project structure will be following:
    
    
    ┏>pollsapi
    ┣━━━━━>crud.py
    ┣━━━━━>database.py
    ┣━━━━━>main.py
    ┣━━━━━>models.py
    ┣━━━━━>schemas.py
    
__database__

*database.py*

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker


    SQLALCHEMY_DATABASE_URL = "postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/DATABASE_NAME"

    engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
    
*models.py*

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
    from sqlalchemy.orm import relationship

    from database import Base


    class Question(Base):
        __tablename__ = "question"
        id = Column(Integer, primary_key=True)
        question_text = Column(String(200))
        pub_date = Column(DateTime)

        choices = relationship('Choice', back_populates="question")


    class Choice(Base):
        __tablename__ = "choice"
        id = Column(Integer, primary_key=True)
        question_id = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'))
        choice_text = Column(String(200))
        votes = Column(Integer, default=0)

        question = relationship("Question", back_populates="choices")

bt doing this we have created ```relationship``` provided by ```SQLAlchemy ORM```. By using it we can simply access ```question.choices``` to get all choices for that particular question.

Simmilarly we can use ```choice.question``` to get question object that is related to that choice.

__Schemas__

*schemas.py*

    from datetime import datetime

    from pydantic import BaseModel
    from typing import List


    # Choice schema

    class ChoiceBase(BaseModel):
        choice_text: str
        votes: int = 0

    class ChoiceCreate(ChoiceBase):
        pass

    class ChoiceList(ChoiceBase):
        id: int

        class Config:
            orm_mode = True


    # Question schema

    class QuestionBase(BaseModel):
        question_text: str
        pub_date: datetime

    class QuestionCreate(QuestionBase):
        pass

    class Question(QuestionBase):
        id: int

        class Config:
            orm_mode = True

    class QuestionInfo(Question):
        choices: List[ChoiceList] = []

Attributes in SQLAlchemy is different than in pydantic. in sqlalchemy they are defined with ```=``` and type is passed in ```Column``` like in:

    question_text = Column(String)
    
while pydantic uses ```:```

    question_text:str
    
Pyndatic models/schemas will be mapped to the incoming data (data in POST, PUT requests) and to the response data returned from the API itself.

We have created base classes ```QuestionBase``` and ```ChoiceBase``` that extends pydantic BaseModel to hold attributes which are common for creating or reading data and created other classes that inherit from these base classes, the reason being we want specific attributes for creation and reading.

like for example - for creating a choice we need ```choice_text``` and votes (if not passed, it defaults to 0) so we will use ```ChoiceCreate``` and for reading the choice, we want to return id, ```choice_text``` and votes and in this case we will use ```ChoiceList```.

Another important thing to understand is the use of ```orm_mode = True```, notice we have added a ```class Config``` and have set orm_mode = True, this is because by default Pydantic model could read the data from dict and it can’t read the data if the data is an ORM model so with the orm_mode = True added to our class, Pydantic model can also read the data from the object something like ```data.question_text```.

Ok, we will now create ```pollsapi/crud.py``` which will contain all the functions to perform ```CRUD``` (```C```reate, 
```R```etrieve, 
```U```pdate 
and ```D```elete) operations.

*crud.py*

    from sqlalchemy.orm import Session

    from models import Base, Question, Choice
    import schema

    # Question

    def create_question(db: Session, question: schema.QuestionCreate):
        obj = Question(**question.dict())
        db.add(obj)
        db.commit()
        return obj

    def get_all_questions(db: Session):
        return db.query(Question).all()

    def get_question(db:Session, qid):
        return db.query(Question).filter(Question.id == qid).first()

    def edit_question(db: Session, qid, question: schema.QuestionCreate):
        obj = db.query(Question).filter(Question.id == qid).first()
        obj.question_text = question.question_text
        obj.pub_date = question.pub_date
        db.commit()
        return obj

    def delete_question(db: Session, qid):
        db.query(Question).filter(Question.id == qid).delete()
        db.commit()

    # Choice

    def create_choice(db:Session, qid: int, choice: schema.ChoiceCreate):
        obj = Choice(**choice.dict(), question_id=qid)
        db.add(obj)
        db.commit()
        return obj

    def update_vote(choice_id: int, db:Session):
        obj = db.query(Choice).filter(Choice.id == choice_id).first()
        obj.votes += 1
        db.commit()
        return obj
        
with this file we have created all the utility functions which will be used in the API .

Now we'll make ```pollsapi/main.py```, which will make use of all the files we created above.

__Create a poll question__

*main.py*

    from fastapi import FastAPI, HTTPException, Response, Depends
    import schema
    from typing import List

    from sqlalchemy.orm import Session

    import crud
    from database import SessionLocal, engine
    from models import Base

    Base.metadata.create_all(bind=engine)

    app = FastAPI()

    # Dependency
    def get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()


    ## Question

    @app.post("/questions/", response_model=schema.QuestionInfo)
    def create_question(question: schema.QuestionCreate, db: Session = Depends(get_db)):
        return crud.create_question(db=db, question=question)


+ line ```Base.metadata.create_all(bind=engine)``` creates database tables utilizing SQLAlchemy models defined above in ```models.py```

+ function ```create_question``` is decorated using the ```app``` object created above which is an instance of ```FastAPI```, it takes two arguments ```path``` and ```response_model```. response_model returns the schema ```QuestionInfo``` so the endpoint will return the fields ```id```, ```question_text``` and ```pub_date```.

+ We have created a function ```create_question```, first argument receives the request data and maps it to the schema ```QuestionCreate``` which has the fields ```question_text``` and ```pub_date``` and the second argument creates a session/request and then it gets closed after the request is completed.

now visit:

    http:127.0.0.1/docs
    
you should see something section to POST /questions/ something like this:

![img](assets/img/fastapidocs.png)

click on that section and it will expand, now click on ```Try it out``` to test your shiny new API.

__List all poll questions__

We will now create an endpoint to get all our poll questions, for this we will use ```@app.get```, add another function in ```pollsapi/main.py```

    @app.get("/questions/", response_model=List[schema.Question])
    def get_questions(db: Session = Depends(get_db)):
        return crud.get_all_questions(db=db)
        
notice the use of ```List``` in ```response_model```, ```crud.get_all_questions``` returns a list of objects and not just an object so we should let our framework know that. if we remove the List our API will throw an error. At this point when you visit:

    http://127.0.0.1:8000/docs
    
you should see two sections:

- ```POST /questions/``` and 
- ```GET /questions/``` 

click on GET section and Try it out and you should see a response something like below:

    [
    {
        "question_text": "What is fastAPI?",
        "pub_date": "2020-05-14T12:58:05.043000",
        "id": 1
    }
    ]
    
__ Retrieve, Edit and Delete a poll question__

    def get_question_obj(db, qid):
        obj = crud.get_question(db=db, qid=qid)
        if obj is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return obj

    @app.get("/questions/{qid}", response_model=schema.QuestionInfo)
    def get_question(qid: int, db: Session = Depends(get_db)):
        return get_question_obj(db=db, qid=qid)
        
    @app.put("/questions/{qid}", response_model=schema.QuestionInfo)
    def edit_question(qid: int, question: schema.QuestionCreate, db: Session = Depends(get_db)):
        get_question_obj(db=db, qid=qid)
        obj = crud.edit_question(db=db, qid=qid, question=question)
        return obj

    @app.delete("/questions/{qid}")
    def delete_question(qid: int, db: Session = Depends(get_db)):
        get_question_obj(db=db, qid=qid)
        crud.delete_question(db=db, qid=qid)
        return {"detail": "Question deleted", "status_code": 204}

Notice how we have used different response_model for ```get_questions``` and ```get_question```, this is because we wanted to show choices in the API response only in case of ```Question detail API``` and not for ```Question list API```.


__create choice for a particular poll question__

    @app.post("/questions/{qid}/choice", response_model=schema.ChoiceList)
    def create_choice(qid: int, choice: schema.ChoiceCreate, db: Session = Depends(get_db)):
        get_question_obj(db=db, qid=qid)
        return crud.create_choice(db=db, qid=qid, choice=choice)
        
__Update votes for question__

    @app.put("/choices/{choice_id}/vote", response_model=schema.ChoiceList)
    def update_vote(choice_id: int, db: Session = Depends(get_db)):
        return crud.update_vote(choice_id=choice_id, db=db)
        
__Endpoints__

the following are the endpoints for Question and Choice


- *Create* question - ```POST http://127.0.0.1:8000/questions/```

- *List* all questions - ```GET http://127.0.0.1:8000/questions/```

- *Retrieve* a particular question - ```GET http://127.0.0.1:8000/questions/{qid}```

- *Edit* a particular question - ```PUT http://127.0.0.1:8000/questions/{qid}```

- *Delete* a particular question - ```DELETE http://127.0.0.1:8000/questions/{qid}```

- *Create* choice for a particular poll question - ```POST http://127.0.0.1:8000/questions/{qid}/choice```

- *Update* votes for a particular question - ```PUT http://127.0.0.1:8000/choices/{choice_id}/vote```

__source code__

You can find source code [here](https://github.com/andrijaJ01/pollsapi)

