//滚动条
changeMsgWrap();
$('#msgMain').jScrollPane({ scrollArea: document });
clientMenu();

/**
 * 软件中的配置，增加连接
 */
function clientMenu() {
    var search = window.location.hash.split('#');
    if (!search || !search[1]) return false;
    var op = search[1].split('=');
    if (op[0] != 'op' || op[1] != 'menu') return false;
    var stockcode = $('#curCode').val();
    var link = null;
    if (stockcode == '399001')
        link = ' [<a href="../1A0001/index.html#op=menu">上证指数</a>]';
    else if (stockcode = '000001')
        link = ' [<a href="../399001/index.html#op=menu">深证成指</a>]';

    var client = $('#client');
    client.css({
        'font-size': 12,
        'color': '#999',
        'paddingLeft': 10
    });
    client.html(link);
    var menuLink = $('#menuLink a');
    for (var i = 0; i < menuLink.length; i++) {
        var href = $(menuLink[i]).attr('href');
        $(menuLink[i]).attr('href', href + '#op=menu');
    }
}

//换肤
var changeSkin = function() {
    tagStat('skin');
    var cssMaster = $("#css_master");
    var cssSkin = $("#css_skin");
    var cssScroll = $("#css_scroll");
    var cssReset = $("#css_reset");
    var f10Skin = GetCookie('f10_skin');
    if (!f10Skin || f10Skin == "dark") {
        $(cssMaster).attr("href", "//s.thsi.cn/css/basic/fundstock/light/master.css?12");
        $(cssSkin).attr("href", "//s.thsi.cn/css/basic/fundstock/light/skin.css?12");
        $(cssScroll).attr("href", "//s.thsi.cn/css/basic/fundstock/light/jScrollPane.css");
        SetCookie('f10_skin', 'white', 24);
        changeRzrqChartSkin('white')
    } else {
        $(cssMaster).attr("href", "//s.thsi.cn/css/basic/fundstock/dark/master.css?12");
        $(cssSkin).attr("href", "//s.thsi.cn/css/basic/fundstock/dark/skin.css?12");
        $(cssScroll).attr("href", "//s.thsi.cn/css/basic/fundstock/dark/jScrollPane.css");
        SetCookie('f10_skin', 'dark', 24);
        changeRzrqChartSkin('dark')
    }
}

//得到用户的默认SKIN
var f10Skin = GetCookie('f10_skin');
if (f10Skin == 'white') {
    var cssMaster = $("#css_master");
    var cssSkin = $("#css_skin");
    if (f10Skin == '' || f10Skin == 'dark') {
        $(cssMaster).attr("href", "//s.thsi.cn/css/basic/fundstock/dark/master.css?12");
        $(cssSkin).attr("href", "//s.thsi.cn/css/basic/fundstock/dark/skin.css?12");
    } else {
        $(cssMaster).attr("href", "//s.thsi.cn/css/basic/fundstock/light/master.css?12");
        $(cssSkin).attr("href", "//s.thsi.cn/css/basic/fundstock/light/skin.css?12");
    }
}

//用户错报框
$(".error").click(function() {
    var _tagName = $("#curName").val();
    var _name = $('#nameHide').val();
    var _code = $('#codeHide').val();
    var _errorBox = [
        '<div class="error-box" id="errorBox">',
        '<div class="title"><span class="close-botton fr over">&nbsp;</span></div>',
        '<div class="conts">',
        '<p>所在栏目：<em id="tag">', _tagName, '</em></p><p>错误描述：<em>(您还可以输 <span id="stringNum">90</span> 字)</em> </p>',
        '<textarea class="textarea-box input-over"></textarea>',
        '<p>请留下您的联系方式，方便我们向您反馈报错处理结果 </p>',
        '<textarea class="textarea-box-contact" value="">请在此输入您的联系方式(手机、邮箱、QQ均可)</textarea>',
        '<p class="tac mt10"><input type="submit" class="input-botton" value=""></p>',
        '</div>',
        '</div>'
    ].join('');
    var _top = $(this).offset().top;
    var _left = $(this).offset().left - 300;
    $(_errorBox).appendTo('body');
    var errorBox = $("#errorBox");
    errorBox.css({
        top: _top,
        left: _left,
        zIndex: 10,
        position: 'absolute'
    });
});

//最大90字符
$("body").delegate('.textarea-box', 'keyup', function() {
    var content = $(this).val();
    var len = 90 - content.length;
    if (len <= 0) {
        $(this).val(content.substring(0, 90));
        $("#stringNum").html(0);
    } else {
        $("#stringNum").html(len);
    }
});

//输入框互换
$("body").delegate('.textarea-box', 'click', function() {
    $(this).attr("class", "textarea-box input-over");
    $(".textarea-box-contact").attr("class", "textarea-box-contact");
});

//点击联系地址
$("body").delegate('.textarea-box-contact', 'click', function() {
    var content = $(this).val();
    if (content == '请在此输入您的联系方式(手机、邮箱、QQ均可)') {
        $(this).val('');
    }
    $(this).attr("class", "textarea-box-contact input-over");
    $(".textarea-box").attr("class", "textarea-box");
});

//关闭
$("body").delegate('.close-botton', 'click', function() {
    $('#errorBox').remove();
});

//提交
$("body").delegate('.input-botton', 'click', function() {
    var _tag = $("#errorBox").find("#tag").html();
    var _name = $('#nameHide').val();
    var _code = $('#codeHide').val();
    var _content = $(".textarea-box").val();
    var _tel = $(".input-box").val();

    if (_tel == "请在此输入您的联系方式(手机、邮箱、QQ均可)") {
        alert('请输入联系方式');
        return false;
    }

    if (_content == '') {
        alert('内容不能为空');
        return false;
    }

    var _postData = [
        'content=', _content,
        '&name=', _name,
        '&code=', _code,
        '&tag=', _tag,
        '&tel=', _tel
    ].join('');

    $.ajax({
        url: '/csiReport.php',
        type: 'POST',
        dateType: 'text',
        data: _postData,
        timeout: 1000,
        success: function(text) {
            alert('提交成功,谢谢');
        },
        error: function() {
            alert('提交失败,请重试');
        }
    });
    $('#errorBox').remove();
});

//新闻点击统计
$(".mode_ul a").click(function() {
    var curId = $("#curId").val();
    TA.log({ 'id': curId, _top: false, 'nopv': true, 'tag': 'csi_news' });
});

//统计
function tagStat(tagName) {
    var curId = $("#curId").val();
    TA.log({ 'id': curId, _top: false, 'nopv': true, 'tag': "csi_" + tagName });
}

/**
 * 滚动条 
 * 
 * @param comtName
 * @return
 */
function changeMsgWrap(comtName) {
    comtName = comtName || $('#releaseMain:visible, #replyMain:visible');
    $('#msgMain').css({ 'height': ($(window).height() - $(comtName).height() - 70) + 'px' });
}

//客户端弹出窗口
function activeTransparent(url) {
    try {
        var thsUtil = external.createObject('Util');
        thsUtil.showWebDlg({ url: url, modeless: 1 });
    } catch (e) {
        alert('请下载客户端');
    }
}