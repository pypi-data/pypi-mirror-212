import glob
import os
from datetime import datetime
from google.cloud import storage
from time_util import MACROS


def upload_to_bucket(src_path, dest_bucket_name, dest_path):
    bucket = storage.Client().bucket("liveramp-eng-qa-reliability")
    if os.path.isfile(src_path):
        blob = bucket.blob(os.path.join(dest_path, os.path.basename(src_path)))
        blob.upload_from_filename(src_path)
        return
    for item in glob.glob(src_path + '/*'):
        if os.path.isfile(item):
            if item == ".keep":
                continue
            blob = bucket.blob(os.path.join(dest_path, os.path.basename(item)))
            blob.upload_from_filename(item)
        else:
            upload_to_bucket(item, dest_bucket_name, os.path.join(dest_path, os.path.basename(item)))


def upload_files():
    bucket = storage.Client().bucket("select-eng-us-2pqa-iris")
    prefix = (f"quality/")
    for filename in os.listdir('reports'):
        bucket.blob(f"{prefix}{filename}").upload_from_filename(f"./reports/{filename}")


def upload_main():
    # bucket = storage.Client().bucket(os.environ['CLIENT_BUCKET'])
    bucket = storage.Client().bucket("select-eng-us-2pqa-iris")
    prefix = (f"quality/logs/test_login/")
    for filename in os.listdir('reports'):
        if filename == ".keep":
            continue
        bucket.blob(f"{prefix}{filename}").upload_from_filename(f"./reports/{filename}")


def upload_lrone_reports():
    now_string = MACROS["now"]
    if not os.environ.get('ENVCHOICE'):
        os.environ['ENVCHOICE'] = "prod"
    envValue = os.environ["ENVCHOICE"]
    if not os.environ.get('JENKINS_TT'):
        os.environ['JENKINS_TT'] = now_string
    jenkins_tt = os.environ["JENKINS_TT"]
    print("************Upload reports******************")
    date_object = datetime.strptime(now_string, '%Y%m%d%H%M%S')
    prefix = date_object.strftime("quality/lrone_automation/{}/reports/".format(jenkins_tt))
    upload_to_bucket("./reports", 'liveramp-eng-qa-reliability', prefix)
    # print("*************Insert results in BigQuery*****************")
    # report_content = read_json_report('../reports/report.json')
    # testcases = report_content["tests"]
    # print("There are {} cases in total.".format(len(testcases)))
    # for item in testcases:
    #     testcase = deal_api_json(item)
    #     insert_case_run_report_table(envValue, testcase)


if __name__ == '__main__':
    upload_lrone_reports()
