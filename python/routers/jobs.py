from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from python.database import get_db
from python.dependencies import get_current_user
from python.models import Job, User
from python.schemas import JobCreate, JobResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/", response_model=JobResponse)
def create_job(
    job: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_job = Job(
        company=job.company,
        role=job.role,
        location=job.location,
        status=job.status ,
        user_id=current_user.id 
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@router.get("/", response_model=list[JobResponse])
def get_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own jobs"
        )

    return job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own jobs"
        )

    job.company = job_data.company
    job.role = job_data.role
    job.location = job_data.location
    job.status = job_data.status

    db.commit()
    db.refresh(job)

    return job

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own jobs"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }