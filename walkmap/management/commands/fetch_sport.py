import os
import re
import requests
from django.core.management.base import BaseCommand
from walkmap.models import AccidentSpot


API_URL = "https://apis.data.go.kr/B552061/frequentzoneOldman/getRestFrequentzoneOldman"


def clean_spot_name(name: str) -> str:
    # "경기도" 표기 통일, 겹친 공백/괄호 정리
    name = name.replace("경기도 ", "경기 ").strip()
    return re.sub(r"\s+", " ", name)


def extract_gu_name(name: str) -> str:
    # 이천시 읍/면/동 추출 (예: 창전동, 중리동, 부발읍, 장호원읍 등)
    m = re.search(r"이천시\s+([가-힣]+(?:읍|면|동))", name)
    if m:
        return m.group(1)
    for suffix in ("읍", "면", "동"):
        for w in name.split():
            if w.endswith(suffix) and len(w) >= 2 and w != "이천시":
                return w
    return ""


class Command(BaseCommand):
    help = "이천시 보행노인 사고다발지역 API 데이터를 불러와 DB에 저장합니다."

    def handle(self, *args, **options):
        service_key = os.environ.get("DATA_GO_KR_KEY")
        if not service_key:
            self.stderr.write(self.style.ERROR("DATA_GO_KR_KEY 환경변수가 설정되지 않았습니다."))
            return

        total_saved = 0
        for year in range(2015, 2025):
            params = {
                "ServiceKey": service_key,
                "searchYearCd": str(year),
                "siDo": "41",  # 경기도
                "guGun": "",  # 빼면 에러 10 발생
                "type": "json",
                "numOfRows": 100,
                "pageNo": 1,
            }
            res = requests.get(API_URL, params=params, timeout=10)
            data = res.json()

            code = data.get("resultCode")
            if code == "03":  # NODATA
                self.stdout.write(f"[{year}] 데이터 없음 (03)")
                continue
            if code != "00":
                self.stderr.write(self.style.WARNING(f"[{year}] 응답 오류: {code} - {data.get('resultMsg')}"))
                continue

            items = data.get("items", {}).get("item", [])
            if isinstance(items, dict):
                items = [items]

            for item in items:
                spot_nm = clean_spot_name(item["spot_nm"])
                # 이천시 데이터만 저장 (siDo=41 전체에 타 시군이 섞여 올 경우 대비)
                if "이천시" not in spot_nm:
                    continue

                AccidentSpot.objects.update_or_create(
                    spot_cd=item["spot_cd"],
                    year=year,
                    defaults={
                        "spot_nm": spot_nm,
                        "gu_name": extract_gu_name(spot_nm),
                        "occrrnc_cnt": int(item["occrrnc_cnt"]),
                        "caslt_cnt": int(item["caslt_cnt"]),
                        "dth_dnv_cnt": int(item["dth_dnv_cnt"]),
                        "se_dnv_cnt": int(item["se_dnv_cnt"]),
                        "sl_dnv_cnt": int(item["sl_dnv_cnt"]),
                        "lat": float(item["la_crd"]),
                        "lng": float(item["lo_crd"]),
                    },
                )
                total_saved += 1

            self.stdout.write(self.style.SUCCESS(f"[{year}] 처리 완료"))

        self.stdout.write(self.style.SUCCESS(f"총 {total_saved}건 저장/갱신 완료"))
