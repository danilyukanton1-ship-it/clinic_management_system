import asyncio

from db.database import AsyncSessionLocal
from db.unit_of_work import UnitOfWork
from infrastructure.celery import celery_app


async def delete_unverified():
    async with AsyncSessionLocal() as session, UnitOfWork(session) as uow:
        users = await uow.users.get_unverified_user()
        for user in users:
            await uow.users.delete_user(user)


@celery_app.task(name="app.users.tasks.delete_unverified_users")
def delete_unverified_users():
    asyncio.run(delete_unverified())
