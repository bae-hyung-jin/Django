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


