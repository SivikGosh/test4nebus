from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from src.models import (
    Activity,
    Building,
    Organization,
    OrganizationActivity,
    PhoneNumber,
)
from src.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import asyncio


async def add_activity(db: AsyncSession, title: str, parent_id: int = None):
    """Добавление вида деятельности."""
    try:
        activity = Activity(title=title, parent_id=parent_id)
        await activity.set_level(db)
        db.add(activity)
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        print(e)
    finally:
        await db.close()


async def add_building(db: AsyncSession, address: str, longitude: float, latitude: float):
    """Добавление здания."""
    try:
        point = from_shape(Point(longitude, latitude), srid=4326)
        building = Building(address=address, location=point)
        db.add(building)
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(e)
    finally:
        await db.close()


async def add_organization(db: AsyncSession, title: str, building_id: int):
    """Добавление организации."""
    try:
        organization = Organization(title=title, building_id=building_id)
        db.add(organization)
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(e)
    finally:
        await db.close()


async def add_organization_activity(db: AsyncSession, org_id: str, activity_id: int):
    """Добавление деятельности организации."""
    try:
        organization_activity = OrganizationActivity(
            organization_id=org_id,
            activity_id=activity_id
        )
        db.add(organization_activity)
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(e)
    finally:
        await db.close()


async def add_phone_number(db: AsyncSession, number: str, org_id: int):
    """Добавление номера телефона организации."""
    try:
        phone_number = PhoneNumber(number=number, organization_id=org_id)
        db.add(phone_number)
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(e)
    finally:
        await db.close()


async def main():
    db = AsyncSessionLocal()

    activities = [
        ('Разработка программного обеспечения', None),  # 1
        ('Веб-разработка', 1),  # 2
        ('Frontend', 2),  # 3
        ('React-приложения', 3),  # 4
        ('Backend', 2),  # 5
        ('REST API', 5),  # 6
        ('Мобильная разработка', 1),  # 7
        ('Android', 7),  # 8
        ('Kotlin-приложения', 8),  # 9
        ('iOS', 7),  # 10
        ('Swift-приложения', 10),  # 11
        ('Консалтинг', None),  # 12
        ('IT-консалтинг', 12),  # 13
        ('Внедрение систем', 13),  # 14
        ('CRM-системы', 14),  # 15
        ('Аудит IT-инфраструктуры', 13),  # 16
        ('Безопасность', 16),  # 17
        ('Бизнес-консалтинг', 12),  # 18
        ('Оптимизация процессов', 18),  # 19
        ('Lean-подход', 19),  # 20
        ('Финансовое планирование', 18),  # 21
        ('Бюджетирование', 21),  # 22
        ('Образование и обучение', None),  # 23
        ('Онлайн-обучение', 23),  # 24
        ('Программирование', 24),  # 25
        ('Python', 25),  # 26
        ('Дизайн', 24),  # 27
        ('UX/UI', 27),  # 28
        ('Внутреннее обучение', 23),  # 29
        ('Обучение сотрудников', 29),  # 30
        ('Soft Skills', 30),  # 31
        ('Повышение квалификации', 29),  # 32
        ('Сертификации', 32),  # 33
    ]
    for title, parent in activities:
        await add_activity(db, title, parent)

    buildings = [
        ('г. Москва, ул. Ленина, 1', 55.7558, 37.6173),
        ('г. Санкт-Петербург, ул. Пушкина, 10', 59.9343, 30.3351),
        ('г. Екатеринбург, пр. Мира, 15', 56.8389, 60.6057),
        ('г. Волгоград, ул. Гагарина, 25', 48.7071, 44.5166),
        ('г. Уфа, ул. Советская, 5', 54.7388, 55.9721),
        ('г. Владивосток, ул. Кирова, 8', 43.1056, 131.8735),
        ('г. Пермь, пр. Победы, 12', 58.0105, 56.2502),
        ('г. Воронеж, ул. Карла Маркса, 3', 51.6608, 39.2003),
        ('г. Тюмень, ул. Жукова, 20', 57.1522, 65.5272),
        ('г. Самара, ул. Комсомольская, 6', 53.1959, 50.1008),
    ]
    for address, longitude, latitude in buildings:
        await add_building(db, address, longitude, latitude)

    organizations = [
        ('АО «ТехноРесурс»', 3),
        ('ООО «ЗенитТранс»', 7),
        ('ПАО «ИнфоТек»', 5),
        ('ООО «АльфаСтрой»', 1),
        ('АО «БетаХолдинг»', 9),
        ('ООО «ГлобалМаркет»', 4),
        ('ЗАО «ЛидерСофт»', 8),
        ('ООО «ВостокЭнерго»', 2),
        ('ПАО «ФинТраст»', 6),
        ('ООО «ДельтаЛогистика»', 10),
        ('АО «КвадроСистемс»', 7),
        ('ООО «ПротонСервис»', 1),
        ('ЗАО «ЭкспертАналитика»', 9),
        ('ООО «ЭкоГрупп»', 3),
        ('ПАО «МегаполисСтрахование»', 6),
        ('ООО «СтройПарк»', 5),
        ('АО «НордИнвест»', 4),
        ('ООО «СигмаПроект»', 2),
        ('ООО «ТехЭлектро»', 8),
        ('ЗАО «АвтоТрек»', 7),
        ('ООО «ИнтерСвязь»', 1),
        ('АО «ГринПлант»', 3),
        ('ПАО «ФармаЛайн»', 9),
        ('ООО «ЛайтГрупп»', 6),
        ('ЗАО «ЦентрПрофи»', 5),
        ('ООО «АйТиЛаб»', 10),
        ('АО «СпектрРешения»', 2),
        ('ООО «ГрузСервис»', 4),
        ('ЗАО «ДетальМаш»', 8),
        ('ПАО «МедиаПоток»', 7),
        ('ООО «ФлексИнжиниринг»', 3),
        ('АО «КейСолюшнс»', 1),
        ('ООО «БизнесРу»', 9),
        ('ЗАО «ТрейдГарант»', 6),
        ('ООО «АгроТраст»', 5),
        ('ПАО «СкайНет»', 2),
        ('АО «ИнжТехСервис»', 8),
        ('ООО «ГрадПроект»', 4),
        ('ЗАО «ФинансСоюз»', 10),
        ('ООО «ЛогикаСофт»', 7),
        ('АО «ЭнергоСистемы»', 1),
        ('ООО «ТрейдСфера»', 3),
        ('ЗАО «СоларЭко»', 9),
        ('ООО «МирАвто»', 6),
        ('АО «РитмМедиа»', 5),
        ('ООО «ЦифраПлюс»', 2),
        ('ПАО «БайкалТур»', 8),
        ('ООО «АйсКом»', 4),
        ('ЗАО «ЭкоВизион»', 10),
        ('ООО «ТехноИмпульс»', 7),
    ]
    for title, building in organizations:
        await add_organization(db, title, building)

    organization_activities = [
        (22, 5), (14, 12), (9, 1), (27, 33), (50, 8),
        (7, 20), (7, 19), (33, 7), (11, 11), (43, 28),
        (26, 25), (18, 6), (41, 3), (4, 10), (22, 30),
        (9, 21), (14, 17), (44, 14), (1, 4), (28, 9),
        (19, 27), (38, 23), (11, 22), (8, 16), (27, 15),
        (30, 18), (22, 2), (37, 13), (5, 24), (50, 32),
        (6, 31), (14, 29), (21, 26), (18, 1), (13, 3),
        (39, 12), (25, 7), (11, 5), (29, 19), (12, 8),
        (7, 11), (15, 20), (30, 10), (49, 4), (10, 14),
        (27, 6), (14, 25), (45, 22), (33, 17), (8, 15),
        (16, 9), (5, 13), (26, 21), (40, 2), (19, 7),
        (44, 3), (11, 30), (22, 11), (27, 24), (6, 28),
        (13, 1), (9, 33), (15, 8), (23, 14), (42, 26),
        (35, 5), (3, 12), (20, 17), (8, 22), (39, 25),
        (41, 6), (50, 10), (24, 19), (17, 31), (7, 4),
        (32, 15), (14, 23), (36, 27), (18, 2), (44, 9),
        (2, 20), (12, 7), (21, 13), (30, 16), (5, 30),
        (7, 21), (25, 1), (8, 11), (27, 5), (19, 24),
        (31, 8), (11, 33), (15, 26), (28, 14), (33, 3),
        (10, 22), (29, 10), (20, 19), (4, 6), (38, 25),
    ]
    for organization, activity in organization_activities:
        await add_organization_activity(db, organization, activity)

    phone_numbers = [
        ('1-123-456', 1),
        ('1-123-456-22-33', 1),
        ('2-234-567', 2),
        ('3-345-678', 3),
        ('3-345-678-44-55', 3),
        ('4-456-789', 4),
        ('5-567-890-66-77', 5),
        ('5-567-890', 5),
        ('6-678-901', 6),
        ('7-789-012-88-99', 7),
        ('8-890-123', 8),
        ('8-890-123-11-22', 8),
        ('9-901-234', 9),
        ('0-012-345-33-44', 10),
        ('1-123-456', 11),
        ('1-123-456-55-66', 11),
        ('2-234-567', 12),
        ('3-345-678', 13),
        ('3-345-678-77-88', 13),
        ('4-456-789', 14),
        ('5-567-890-99-11', 15),
        ('5-567-890', 15),
        ('6-678-901', 16),
        ('7-789-012-22-33', 17),
        ('8-890-123', 18),
        ('8-890-123-44-55', 18),
        ('9-901-234', 19),
        ('0-012-345-66-77', 20),
        ('1-123-456', 21),
        ('1-123-456-88-99', 21),
        ('2-234-567', 22),
        ('3-345-678', 23),
        ('3-345-678-11-22', 23),
        ('4-456-789', 24),
        ('5-567-890-33-44', 25),
        ('5-567-890', 25),
        ('6-678-901', 26),
        ('7-789-012-55-66', 27),
        ('8-890-123', 28),
        ('8-890-123-77-88', 28),
        ('9-901-234', 29),
        ('0-012-345-99-11', 30),
        ('1-123-456', 31),
        ('1-123-456-22-33', 31),
        ('2-234-567', 32),
        ('3-345-678', 33),
        ('3-345-678-44-55', 33),
        ('4-456-789', 34),
        ('5-567-890-66-77', 35),
        ('5-567-890', 35),
        ('6-678-901', 36),
        ('7-789-012-88-99', 37),
        ('8-890-123', 38),
        ('8-890-123-11-22', 38),
        ('9-901-234', 39),
        ('0-012-345-33-44', 40),
        ('1-123-456', 41),
        ('1-123-456-55-66', 41),
        ('2-234-567', 42),
        ('3-345-678', 43),
        ('3-345-678-77-88', 43),
        ('4-456-789', 44),
        ('5-567-890-99-11', 45),
        ('5-567-890', 45),
        ('6-678-901', 46),
        ('7-789-012-22-33', 47),
        ('8-890-123', 48),
        ('8-890-123-44-55', 48),
        ('9-901-234', 49),
        ('0-012-345-66-77', 50),
    ]
    for number, organization in phone_numbers:
        await add_phone_number(db, number, organization)


if __name__ == '__main__':
    asyncio.run(main())

# TODO добавить декоратор принта до выполнения функции и после
# TODO добавить игнорирование существующей уже записи
# TODO объединить все функции в одну универсальную
