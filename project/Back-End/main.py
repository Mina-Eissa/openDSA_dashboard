from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from get_result import router as get_result_router
from get_result2 import router as get_result2_router
from student_course_data import router as student_book_data_router
from student_progress import router as student_progress_router
from students_enrolled_in_book import router as students_enrolled_in_book_router
from get_books_data import router as get_books_data_router
from Filtered_IRT import router as filtered_IRT_router
from get_books import router as get_books_router
from students_brief import router as students_brief_router
from Filtered_book import router as filtered_book_router
from Filtered_student_by_exercises import router as filtered_student_by_exercises_router
from get_courses import router as get_courses_router
from get_exercises_from_real_data import router as get_exercises_from_real_data_router
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
app.include_router(get_books_data_router)
app.include_router(filtered_IRT_router)
app.include_router(get_books_router)
app.include_router(students_brief_router)
app.include_router(filtered_book_router)
app.include_router(filtered_student_by_exercises_router)
app.include_router(get_courses_router)
app.include_router(get_exercises_from_real_data_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=4000)
