from django.db import models

# 클래스 선언 과 지점 기본 정보
class AccidentSpot(models.Model):
    spot_cd = models.CharField('지점 코드', max_length=30)
    year = models.IntegerField('발생 연도')
    spot_nm = models.CharField('지점명', max_length=200)
    gu_name = models.CharField('구', max_length=20, blank=True, default='')

    # 사고건수 및 좌표필드
    occrrnc_cnt = models.IntegerField('발생 건수', default=0)
    caslt_cnt = models.IntegerField('사상자 수', default=0)
    dth_dnv_cnt = models.IntegerField('사망자 수', default=0)
    se_dnv_cnt = models.IntegerField('중상자 수', default=0)
    sl_dnv_cnt = models.IntegerField('경상자 수', default=0)

    lat = models.FloatField('위도')
    lng = models.FloatField('경도')
    
    # 중복 방지를 위해 spot_cd와 year를 유니크 제약조건으로 설정
    class Meta:
        ordering = ['-year', '-occrrnc_cnt']
        constraints = [
            models.UniqueConstraint(
                fields=['spot_cd', 'year'],
                name='unique_walkmap_spot_year',
            )
        ]

    def __str__(self):
        return f'[{self.year}] {self.spot_nm} (발생 {self.occrrnc_cnt}건)'


# 이천시 횡단보도 모델 (전국횡단보도표준데이터 연동)
class Crosswalk(models.Model):
    manage_no = models.CharField('횡단보도 관리번호', max_length=50, unique=True)
    road_nm = models.CharField('도로명', max_length=100, blank=True, default='')
    address = models.CharField('소재지 주소', max_length=200, blank=True, default='')
    length = models.FloatField('횡단보도 연장(m)', default=0.0)  # et (보행 거리)
    width = models.FloatField('횡단보도 폭(m)', default=0.0)   # bt
    lanes = models.IntegerField('차로 수', default=0)         # cartrkCo
    has_signal = models.BooleanField('보행자신호등 유무', default=False)  # tfclghtYn
    lat = models.FloatField('위도')
    lng = models.FloatField('경도')

    class Meta:
        ordering = ['road_nm', 'address']
        verbose_name = '횡단보도'
        verbose_name_plural = '횡단보도 목록'

    def __str__(self):
        return f'{self.road_nm or self.address} ({self.length}m)'


