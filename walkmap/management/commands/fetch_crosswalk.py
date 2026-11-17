import os
import requests
from django.core.management.base import BaseCommand
from walkmap.models import Crosswalk

API_URL = "https://api.data.go.kr/openapi/tn_pubr_public_crosswalk_api"


class Command(BaseCommand):
    help = "이천시 전국횡단보도표준데이터 API를 불러와 DB에 저장합니다."

    def handle(self, *args, **options):
        service_key = os.environ.get("DATA_GO_KR_KEY")
        if not service_key:
            self.stderr.write(self.style.ERROR("DATA_GO_KR_KEY 환경변수가 설정되지 않았습니다."))
            return

        page_no = 1
        num_of_rows = 100
        total_saved = 0

        while True:
            params = {
                "serviceKey": service_key,
                "pageNo": str(page_no),
                "numOfRows": str(num_of_rows),
                "type": "json",
                "signguNm": "이천시",
            }
            try:
                res = requests.get(API_URL, params=params, timeout=15)
                data = res.json()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"요청 실패 (page {page_no}): {e}"))
                break

            header = data.get("header", {})
            if header.get("resultCode") != "00":
                self.stderr.write(self.style.WARNING(f"응답 오류: {header.get('resultCode')} - {header.get('resultMsg')}"))
                break

            body = data.get("body", {})
            items = body.get("items", {}).get("item", [])
            if isinstance(items, dict):
                items = [items]

            if not items:
                break

            for item in items:
                manage_no = item.get("crslkManageNo")
                if not manage_no:
                    continue

                try:
                    lat = float(item.get("latitude") or 0)
                    lng = float(item.get("longitude") or 0)
                except ValueError:
                    continue

                if lat == 0 or lng == 0:
                    continue

                try:
                    length = float(item.get("et") or 0)
                except ValueError:
                    length = 0.0

                try:
                    width = float(item.get("bt") or 0)
                except ValueError:
                    width = 0.0

                try:
                    lanes = int(item.get("cartrkCo") or 0)
                except ValueError:
                    lanes = 0

                road_nm = (item.get("roadNm") or "").strip()
                address = (item.get("lnmadr") or item.get("rdnmadr") or "").strip()
                has_signal = (item.get("tfclghtYn") or "N").strip().upper() == "Y"

                Crosswalk.objects.update_or_create(
                    manage_no=manage_no,
                    defaults={
                        "road_nm": road_nm,
                        "address": address,
                        "length": length,
                        "width": width,
                        "lanes": lanes,
                        "has_signal": has_signal,
                        "lat": lat,
                        "lng": lng,
                    },
                )
                total_saved += 1

            self.stdout.write(f"Page {page_no} 처리 완료 ({len(items)}건)")

            total_count = int(body.get("totalCount") or 0)
            if page_no * num_of_rows >= total_count:
                break
            page_no += 1

        self.stdout.write(self.style.SUCCESS(f"이천시 횡단보도 총 {total_saved}건 저장/갱신 완료"))
