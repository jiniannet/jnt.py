import unittest
from jntemplate import Template, engine


class Nodetest(unittest.TestCase):
    def test_foreach(self):
        text = "${foreach(i in list)}${i}${end}"
        template = Template(text)
        template.set("list", [7, 0, 2, 0, 6])
        render = template.render()
        self.assertEqual("70206", render)

    def test_negative(self):
        text = "$test(8,-2)"
        template = Template(text)
        template.set("test", lambda x, y: x + y)
        render = template.render()
        self.assertEqual(6, float(render))

    def test_set(self):
        text = "$set(aGroupName = \"Begin\"+value)$aGroupName"
        template = Template(text)
        template.set("value", 30)
        render = template.render()
        self.assertEqual("Begin30", render)

    def test_variable(self):
        text = "($a)人"
        template = Template(text)
        template.set("a", "1")
        render = template.render()
        self.assertEqual("(1)人", render)

    def test_expression(self):
        text = "${8+2*5}"
        template = Template(text)
        render = template.render()
        self.assertEqual(18, float(render))

    def test_expression1n(self):
        text = "${3000-0-1000-0}"
        template = Template(text)
        render = template.render()

        self.assertEqual(2000, float(render))

    def test_expressio3(self):
        text = "${3000-1000+200-20}"
        template = Template(text)
        render = template.render()
        self.assertEqual(2180, float(render))

    def test_expressio4(self):
        text = "${3000-1000+8-8+8-8}"
        template = Template(text)
        render = template.render()
        self.assertEqual(2000, float(render))

    def test_Expressio5(self):
        text = "${10000 + 2 *  4 * 10}"
        template = Template(text)
        render = template.render()
        self.assertEqual(10080, float(render))

    def test_Expressio6(self):
        text = "${10000 != 0 +  0 + 10000}"
        template = Template(text)
        render = template.render()

        self.assertEqual("False", render)

    def test_expressio7(self):
        text = "${10000 * 2 + 2 *  4 * 10 / 8 - 24 + 0 + 0 + 0 + 0 * 1 * 2 * 3 * 4}"
        template = Template(text)
        render = template.render()

        self.assertEqual(19986, float(render))

    def test_complicated_expression(self):
        text = "${(8+2)*(5+5) - ((2+8)/2)}"
        template = Template(text)
        render = template.render()
        self.assertEqual(95,  float(render))

    def test_logic_expression(self):
        text = "${4<=5}"
        template = Template(text)
        render = template.render()
        self.assertEqual("True", render)

    def test_or_expression(self):
        text = "${4==5||5==5}"
        template = Template(text)
        render = template.render()

        self.assertEqual("True", render)

    def test_and_expression(self):
        text = "${4==5&&5==5}"
        template = Template(text)
        render = template.render()

        self.assertEqual("False", render)

    def test_if(self):
        text = "${if(3==8)}3=8 success${elseif(3>8)}3>8 success${elseif(2<5)}2<5 success${else}null${end}"
        template = Template(text)
        render = template.render()
        self.assertEqual("2<5 success", render)

    # def test_if1(self):
    #     text = "$if(CreteDate >= date.AddDays(-3))yes$end" //数组取值用get即可取到 List<Int32>用get_Item  见.NET的索引实现原理
    #     template = Template(text)
    #     template.set("CreteDate", DateTime.Now)
    #     template.set("date", DateTime.Now)
    #     render = template.render()
    #     self.assertEqual("yes", render)

    def test_if2(self):
        text = "${if(dd)}yes${else}no$end"
        template = Template(text)
        template.set("dd", object())

        render = template.render()
        self.assertEqual("yes", render)

    def test_if3(self):
        text = "$if(3>2 && 5<2)yes${else}no${end}"
        template = Template(text)
        render = template.render()
        self.assertEqual("no", render)

    def test_if4(self):
        text = "$if(v1 || 5<2)yes${else}no${end}"
        template = Template(text)
        render = template.render()
        self.assertEqual("no", render)

    def test_if5(self):
        text = "$if(v1 || v2)yes${else}no${end}"
        template = Template(text)
        template.set("v2", 9)
        render = template.render()
        self.assertEqual("yes", render)

    # def test_For(self):
    #     text = "$for(i=1i<4i=i+1)${i}$end"
    #     template = Template(text)
    #     render = template.render()
    #     self.assertEqual("123", render)


#     def test_For1(self):
#         text = "$for(i=0i<3i++)${i}$end"//"$for(i=1i<4i=i+1)${i}$end"
#         template = Template(text)
#         render = template.render()

#         self.assertEqual("012", render)

    def test_reference(self):
        text = "$str.upper()"
        template = Template(text)
        template.set("str", "hello jnt4py")
        render = template.render()
        self.assertEqual("HELLO JNT4PY", render)

#     /// <summary>
#     /// 测试索引取值与方法标签
#     /// </summary>
#
#     def test_IndexValue(self):
#         text = "$data.Get(0)" //数组取值用get即可取到 List<Int32>用get_Item  原因见.NET的索引实现原理
#         template = Template(text)

#         template.set("data", new int[] { 7, 0, 2, 0, 6 })
#         render = template.render()
#         self.assertEqual("7", render)
#     }

#     /// <summary>
#     /// 测试索引取值与方法标签
#     /// </summary>
#
#     def test_IndexValue1(self):
#     {
#         text = "$data.get_Item(\"name\")"
#         template = Template(text)
#         var dic = new System.Collections.Generic.Dictionary<string, string>()
#         dic["name"] = "你好！jntemplate"
#         dic["age"] = "1"
#         template.set("data", dic)
#         render = template.render()
#         self.assertEqual("你好！jntemplate", render)
#     }

#     /// <summary>
#     /// 测试索引取值与方法标签
#     /// </summary>
#
#     def test_IndexValue2(self):
#     {
#         text = "$data.name"//索引也可以和属性一样取值，不过推荐用get_Item，且如果索引是数字时，请尽量使用$data.get_Item(index)
#         template = Template(text)
#         var dic = new System.Collections.Generic.Dictionary<string, string>()
#         dic["name"] = "你好！jntemplate"
#         dic["age"] = "1"
#         template.set("data", dic)
#         render = template.render()
#         self.assertEqual("你好！jntemplate", render)
#     }

#     /// <summary>
#     /// 测试索引取值与方法标签
#     /// </summary>
#
#     def test_IndexValue3(self):
#     {
#         text = "$data.get_Item(0)" //数组取值用get即可取到 List<Int32>用get_Item  见.NET的索引实现原理
#         template = Template(text)

#         template.set("data", new System.Collections.Generic.List<int>(new int[] { 7, 0, 2, 0, 6 }))
#         render = template.render()
#         self.assertEqual("7", render)
#     }

#     /// <summary>
#     /// 测试索引取值与方法标签
#     /// </summary>
#
#     def test_Load(self):
#     {
#         text = "$load(\"include/header.txt\")"
#         template = Template(text)
#         template.set("name", "jntemplate")
# #if NETCOREAPP1_1
#         template.Context.CurrentPath = new System.IO.DirectoryInfo(System.AppContext.BaseDirectory).Parent.Parent.Parent.FullName + System.IO.Path.DirectorySeparatorChar.ToString() + "templets" + System.IO.Path.DirectorySeparatorChar.ToString() + "default"
# #else
#         template.Context.CurrentPath = new System.IO.DirectoryInfo(System.Environment.CurrentDirectory).Parent.Parent.FullName + System.IO.Path.DirectorySeparatorChar.ToString() + "templets" + System.IO.Path.DirectorySeparatorChar.ToString() + "default"
# #endif
#         render = template.render()
#         self.assertEqual("你好，jntemplate", render)
#     }

#     /// <summary>
#     /// 测试索引取值与方法标签
#     /// </summary>
#
#     def test_Inclub(self):
#     {
#         text = "$include(\"include/header.txt\")"
#         template = Template(text)
#         template.set("name", "jntemplate")
# #if NETCOREAPP1_1
#         template.Context.CurrentPath = new System.IO.DirectoryInfo(System.AppContext.BaseDirectory).Parent.Parent.Parent.FullName + System.IO.Path.DirectorySeparatorChar.ToString() + "templets" + System.IO.Path.DirectorySeparatorChar.ToString() + "default"
# #else
#         template.Context.CurrentPath = new System.IO.DirectoryInfo(System.Environment.CurrentDirectory).Parent.Parent.FullName + System.IO.Path.DirectorySeparatorChar.ToString() + "templets" + System.IO.Path.DirectorySeparatorChar.ToString() + "default"
# #endif
#         render = template.render()
#         self.assertEqual("你好，$name", render)
#     }

#     /// <summary>
#     /// 自定义标签前后缀测试
#     /// </summary>
#
#     def test_Config(self):
#     {
#         var conf = Configuration.EngineConfig.CreateDefault()
#         conf.TagFlag = '@'
#         conf.TagSuffix = "}"
#         conf.TagPrefix = "{$"

#         Engine.Configure(conf)

#         text = "你好，@name,欢迎来到{$name}的世界"
#         template = (Template)Engine.CreateTemplate(text)
#         template.set("name", "jntemplate")
#         render = template.render()
#         self.assertEqual("你好，jntemplate,欢迎来到jntemplate的世界", render)

#         Engine.Configure(Configuration.EngineConfig.CreateDefault())
#         //self.assertEqual("111", "111")
#     }

    def test_coment(self):
        text = "你好,$*使用简写符加星号可对代码注释*$欢迎使用"
        template = Template(text)
        template.set("name", "jntemplate")
        render = template.render()
        self.assertEqual("你好,欢迎使用", render)


#     /// <summary>
#     /// 测试DataTable
#     /// </summary>
#
#     def test_Table1(self):
#     {
#         var dt = new System.Data.DataTable()
#         dt.Columns.Add("name", typeof(string))
#         var dr = dt.NewRow()
#         dr["name"] = "Han Meimei"

#         dt.Rows.Add(dr)


#         text = "$dt.Rows.get_Item(0).get_Item(\"name\")"
#         template = Template(text)
#         template.set("dt", dt)
#         render = template.render()
#         self.assertEqual("Han Meimei", render)
#     }

#     /// <summary>
#     /// 测试DataTable
#     /// </summary>
#
#     def test_Table2(self):
#     {
#         var dt = new System.Data.DataTable()
#         dt.Columns.Add("name", typeof(string))
#         var dr = dt.NewRow()
#         dr["name"] = "Han Meimei"

#         dt.Rows.Add(dr)


#         text = @"
# $foreach(dr in dt.Rows)
# $dr.get_Item(""name"")
# $end
# "
#         template = Template(text)
#         template.set("dt", dt)
#         render = template.render()
#         self.assertEqual("Han Meimei", render)
#     }

#     /// <summary>
#     /// 测试DataTable
#     /// </summary>
#
#     def test_Table3(self):
#     {
#         var dt = new System.Data.DataTable()
#         dt.Columns.Add("name", typeof(string))
#         var dr = dt.NewRow()
#         dr["name"] = "Han Meimei"

#         dt.Rows.Add(dr)
#         text = @"
# $foreach(dr in dt.Rows)
# $foreach(data in dr.ItemArray)
#     值:$data
# $end
# $end
# "
#         template = Template(text)
#         template.set("dt", dt)
#         render = template.render()
#         self.assertEqual("值:Han Meimei", render)
#     }
#     /// <summary>
#     /// 测试委托方法
#     /// </summary>
#
#     def test_DelegateFunction(self):
#     {
#         text = "$test(\"字符串\",1,true)"
#         template = Template(text)
#         template.set("test", new JinianNet.JNTemplate.FuncHandler(args =>
#         {
#             System.Text.StringBuilder sb = new System.Text.StringBuilder()
#             sb.Append("您输入的参数是有：")
#             foreach (var node in args)
#             {
#                 sb.Append(node)
#                 sb.Append(" ")
#             }
#             return sb.ToString()
#         }))

#         render = template.render()

#         self.assertEqual("您输入的参数是有：字符串 1 True ", render)
#     }

#     /// <summary>
#     /// 测试类方法
#     /// </summary>
#
#     def test_ClassFunction(self):
#     {
#         text = "$fun.test_(\"字符串\",1,true)"
#         template = Template(text)
#         template.set("fun", TemplateMethod())
#         render = template.render()
#         self.assertEqual("您输入的参数是有：字符串 1 True ", render)
#     }

# #if !NETCOREAPP1_1
#     /// <summary>
#     /// 测试方法的params参数  .NET core中不支持
#     /// </summary>
#
#     def test_FunctionParams(self):
#     {
#         text = "$fun.test_Params(\"字符串\",1,true)"
#         template = Template(text)
#         template.set("fun", TemplateMethod())
#         render = template.render()
#         self.assertEqual("您输入的参数是有：字符串 1 True ", render)
#     }

#     /// <summary>
#     /// 测试方法的params参数2 .NET core中不支持
#     /// </summary>
#
#     def test_FunctionParams2(self):
#     {
#         text = "$fun.test_Params2(\"您输入的参数是有：\",\"字符串\",1,true)"
#         template = Template(text)
#         template.set("fun", TemplateMethod())
#         render = template.render()
#         self.assertEqual("您输入的参数是有：字符串 1 True ", render)
#     }

# #endif


#     /// <summary>
#     /// 测试字符串转义
#     /// </summary>
#
#     def test_String(self):
#     {
#         text = "$set(str=\"3845254\\\\\\\"3366845\\\\\")$str"
#         template = Template(text)
#         render = template.render()
#         self.assertEqual("3845254\\\"3366845\\", render)

#     }

#     /// <summary>
#     /// 测试标签前后空白字符串处理
#     /// </summary>

    def test_strip_white_space(self):
        text = "\
your data is:\
$set(key1=1)\
$set(key2=2)\
$set(key3=3)\
$set(key4=4)\
$set(key5=5)\
$set(key6=6)\
$key5"
        template = Template(text)
        #template.Context.StripWhiteSpace = true
        render = template.render()
        self.assertEqual("your data is:5.0", render)


#     ///// <summary>
#     ///// 测试标签大小写
#     ///// </summary>
#     //
#     //def test_IgnoreCase()
#     //{
#     //    text  = "$date.Year"
#     //    template = Template(text)
#     //    template.set("date",DateTime.Now)
#     //    render = template.render()
#     //    self.assertEqual(DateTime.Now.Year.ToString(), render)
#     //}

if __name__ == '__main__':
    engine.configure()
    unittest.main()
# python -m unittest mydict_test
