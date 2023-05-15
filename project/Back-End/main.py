from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from get_result import router as get_result_router
from get_result2 import router as get_result2_router
from student_book_data import router as student_book_data_router
from student_progress import router as student_progress_router
from students_enrolled_in_book import router as students_enrolled_in_book_router


app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(students_enrolled_in_book_router)
app.include_router(student_progress_router)
app.include_router(student_book_data_router)
app.include_router(get_result2_router)
app.include_router(get_result_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=4000)
