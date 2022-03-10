import unittest
import os
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction
import time
import datetime
import pandas as pd


class ScanAging(unittest.TestCase):

    def setUp(self):
        # Set up appium
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4723/wd/hub',
            desired_capabilities={
                "platformName": "Android",
                "platformVersion": "11",# 실행할 폰에 맞추어 정보 수정 필요
                "deviceName": "GTA3",# 실행할 폰에 맞추어 정보 수정 필요
                "automationName": "Appium",
                "newCommandTimeout": 3000,
                "appPackage": "com.koamtac.ktsync",
                "appActivity": "com.koamtac.ktsync.MainActivity",
                "udid": "R54R1029CWB",# 실행할 폰에 맞추어 정보 수정 필요
                "noReset": "True"  # app 데이터 유지
            })

    def test_search_field(self):
        # appiun의 webdriver를 초기화 합니다.
        driver = self.driver
        # 테스트 시나리오에 따라 selenium 작성
        sleep(10)
        # Aging Delay 선언
        delay = 1

        #스캔 결과를 추가할 데이터 프레임 생성
        df = pd.DataFrame(columns={"Data", "Time"})
        #실패힛수 0 선언
        sf = 0

        #3회 연속 ScanFail 발생할 때 가지 곗ㄱ 반복
        while sf < 3 :
            # Scan 버튼 누름
            driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView").click()
            try:
                #스캔한 결과값 3초동안 기다림
                wait = WebDriverWait(driver, 3)
                element = wait.until(EC.visibility_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.TextView")))
                #스캔결과 데이터, 시간 나누어 리스트
                scan_result = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.TextView").text
                scan_result_list = scan_result.split(";")
                # print(scan_result_list)
                dic_scan_result = {
                    "Data" : [scan_result_list [0]],
                    "Time" : [scan_result_list [1]]
                }
                df_scan_result = pd.DataFrame(dic_scan_result)
                #데리터프레임에 결과값 딕셔너리 추가
                df = pd.concat([df, df_scan_result])
                #clear 버튼 누르기
                driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.LinearLayout[2]/android.widget.TextView[3]").click()
                #실패횟수 초기화
                sf = 0

            except:
                #DF에 스캔킬패 추가
                dic_scan_fail = {
                    "Data" : ["Scan faied"],
                    "Time" : [""]
                }
                df_sacn_fail = pd.DataFrame(dic_scan_fail)
                df = pd.concat([df, df_sacn_fail])
                #실패 횟수 1회 추가
                sf = sf + 1
                # clear 버튼 누르기
                driver.find_element(By.XPATH,
                                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.LinearLayout[2]/android.widget.TextView[3]").click()

            # sleep(delay)
        #결과값 데이터 프레임 scv파일로 저장
        now = datetime.datetime.now()
        now_date = now.strftime("%Y%m%d")
        df.to_csv("ScanAgingReset_" + now_date + ".csv")



def tearDown(self):
    self.driver.quit()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ScanAging)
    unittest.TextTestRunner(verbosity=2).run(suite)
