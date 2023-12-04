from tortoise.expressions import Q

from database import models


class UserRepository:

    def __init__(self) -> None:
        ...

    @staticmethod
    async def get(tg_id: int | None = None) -> models.User | None:
        if not tg_id:
            raise ValueError("provide one parameter for search")

        user = await models.User.get_or_none(Q(tg_id=tg_id if tg_id else None))
        # |Q(referral_id=referral_id if referral_id else None) |
        # Q(email=email if email else None)

        return user

    @staticmethod
    async def get_or_create(tg_id: int | None = None) -> (models.User, bool):
        if not tg_id:
            raise ValueError("provide one parameter for search")

        user = await models.User.get_or_create(tg_id=tg_id)

        return user

    async def update_necessary(self,
                               tg_id: int,
                               username: str,
                               language_code: str | None = 'en') -> models.User | None:
        if not tg_id and not username:
            raise ValueError("provide one parameter for search")

        user, is_new = await self.get_or_create(tg_id=tg_id)
        user.username = username
        if is_new: user.language_code = language_code
        await user.save()
        return user

    async def update_language_code(self,
                                   tg_id: int,
                                   language_code: str) -> models.User | None:
        user = await self.get(tg_id=tg_id)
        user.language_code = language_code
        await user.save()
        return user
