import arrow
import time
from sqlalchemy.orm import Session

from app.api.schemas import DustCreate
from app.api.models import Dust, Weather_InfoTable
from app.weatherApp.WeatherApi import get_all_api_data


# 미세먼지 관련 함수
# 받을 정보에 따라서 추가 예정

def get_dusts(db: Session):
    return db.query(Dust).all()


def get_dustId(db: Session, dust_id: int = 0):
    return db.query(Dust).get(dust_id)


def create_dust(db: Session, dust: DustCreate):
    measure_time = arrow.utcnow().to('Asia/Seoul').format(arrow.FORMAT_RFC1123)
    db_dust = Dust(CurrentTime=str(measure_time),
                          location=dust.location,
                          DustPm10=dust.DustPm10,
                          DustPm25=dust.DustPm25,
                          Humidity=dust.Humidity,
                          Temperature=dust.Temperature,
                          CarbonMonoxide=dust.CarbonMonoxide,
                          NitrogenDioxide=dust.NitrogenDioxide,
                          Ethanol=dust.Ethanol,
                          Hydrogen=dust.Hydrogen,
                          Ammonia=dust.Ammonia,
                          Methane=dust.Methane,
                          Propane=dust.Propane,
                          IsoButane=dust.IsoButane,
                          )

    db.add(db_dust)
    db.commit()
    db.refresh(db_dust)
    return db_dust


def create_apidata(db: Session):
    now = time.localtime()
    date = f"{now.tm_year}{now.tm_mon:02d}{now.tm_mday:02d}{now.tm_hour:02d}"
    lasttime = ''
    print("Time passed.\nGet the app data")
    result, lasttime = get_all_api_data(date, lasttime)
    lasttime = date
    result['collected_time'] = lasttime
    weather = Weather_InfoTable(
        getHeatFeelingIdx=result['getHeatFeelingIdx'],
        getDiscomfortIdx=result['getDiscomfortIdx'],
        getUVIdx=result['getUVIdx'],
        getSenTaIdx=result['getSenTaIdx'],
        getAirDiffusionIdx=result['getHeatFeelingIdx'],
        SO2=result['SO2'],
        CO=result['CO'],
        O3=result['O3'],
        NO2=result['NO2'],
        PM10=result['PM10'],
        PM25=result['PM25'],
        collected_time=lasttime
    )
    db.add(weather)
    db.commit()
    db.refresh(weather)

    info = db.query(Weather_InfoTable).all()
    return info



