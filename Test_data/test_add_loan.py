import unittest
from ddt import ddt,data
from common.test_log import TestLog
from common.do_test_excel import DoExcel
from common.test_request import TestRequest
from common.test_get_data import GetData

test_data=DoExcel().data_read('add_loan')
# print(test_data)
@ddt
class TestCase(unittest.TestCase):
    def setUp(self):
        '''执行用例前动作'''
        # global resp
        TestLog().info("===============测试开始=====================")
    def tearDown(self):
        '''执行用例后动作'''
        TestLog().info("===============测试结束=====================")

    @data(*test_data)    #将嵌套在列表内的字典格式用例做处理，分别取出字典格式用例并迭代赋值给变量cases
    def test_http_request(self,case):
        global resp
        global TestResult
        Caseid=case['用例序号']
        Module=case['模块']
        Method=case['请求方式']
        Url=case['接口地址']
        Case_name=case['用例名']
        param=eval(case['参数'])
        #传参使用字典格式
        Sql=case['sql']
        Expect_Result=eval(case['预期结果'])
        #字典格式断言预期结果与实际结果

        TestLog().info("正在执行{}模块，第{}条用例,用例名:{}".format(Module,Caseid,Case_name))

        resp = TestRequest().testrequest(Method,Url,param,getattr(GetData,'COOKIES'))
        if resp.cookies:
            setattr(GetData,'COOKIES',resp.cookies)
        #获取请求结果
        try:
            self.assertEqual(eval(case['预期结果']),resp.json())
            #将请求结果转换为字典格式与预期结果对比
            TestResult='PASS'
        except AssertionError as e:
            TestLog().info("断言失败{}".format(e))
            TestResult='FAILED'
            raise e
        finally:
            TestLog().info("回写实际结果：{}".format(resp.text))
            DoExcel().data_write('add_loan',Caseid+1,9,resp.text)
            TestLog().info("预期结果:：{}".format(Expect_Result))
            TestLog().info("回写测试结论：{}".format(TestResult))
            DoExcel().data_write('add_loan',Caseid+1,10,TestResult)





