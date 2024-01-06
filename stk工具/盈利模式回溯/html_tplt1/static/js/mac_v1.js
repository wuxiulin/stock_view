//CPI-PPIï¿½ï¿½ï¿½ï¿½ï¿½ï¿½
/* function _flash_ready(flashId) {
    console.log(flashId)
    var object = document.getElementById(flashId);
    if (flashId == 'cpi_ppi') {
        object.loadJSON(macChart);

        initChart(object)
    } else if (flashId == 'm1_m2') {
        object.loadJSON(mmChart);
    } else if (flashId == 'zbj') {
        //object.loadJSON(zbjChart);
        return zbjChart;
    } else if (flashId == 'interest') {
        //object.loadJSON(interestChart);
        return interestChart;
    }
} */
Array.prototype.forEach = function(callback) {   
    for (var i = 0; i < this.length; i++) {
        callback.apply(this, [this[i], i, this]);
    }
};

				$(function() {  // jQuery 的文档就绪事件，当页面完全加载完毕时执行其中的代码。在这里，它用于设置点击事件监听器。
		    $('.v a').click(function() {  //当某个类为 'v' 下的 a 元素被点击时，会触发下列代码块：
		        color.bgColor = color.bgColor == '#181d24' ? '#fff' : '#181d24'
		       initChart('无标题', color, chat0) 

		    })
		    color = {//在点击事件中，切换背景颜色（黑/白）后，分别调用 initChart 函数初始化四个图表
		        'axisFontColor': '#666',
		        'lineColor': ['#f06f6f', '#7eb2f3', '#fea31e']
		    }
		   initChart('无标题', color, chat0) 

		})
// $(function() {  // jQuery 的文档就绪事件，当页面完全加载完毕时执行其中的代码。在这里，它用于设置点击事件监听器。
//     $('.v a').click(function() {  //当某个类为 'v' 下的 a 元素被点击时，会触发下列代码块：
//         color.bgColor = color.bgColor == '#181d24' ? '#fff' : '#181d24'
//         initChart('cpi_ppi', color, cp)
//         initChart('m1_m2', color, mm)
//         initChart('zbj', color, zbj)
//         initChart('interest', color, interest)
//     })
//     color = {//在点击事件中，切换背景颜色（黑/白）后，分别调用 initChart 函数初始化四个图表
//         'axisFontColor': '#666',
//         'lineColor': ['#f06f6f', '#7eb2f3', '#fea31e']
//     }
//     initChart('cpi_ppi', color, cp)
//     initChart('m1_m2', color, mm)
//     initChart('zbj', color, zbj)
//     initChart('interest', color, interest)
// })

function initChart(id, color, data, opt) {//这个函数用于初始化 ECharts 图表。根据传入的参数，配置图表的样式、数据等信息。
    var data3 = {
        name: '',
        data: []
    };
    var unit = false
    var data1 = data[0];
    var data2 = data[1];
    if (id == 'zbj' || id == 'interest') {
        unit = true
        data3 = data[2]
    }
    var myChart = echarts.init(document.getElementById(id));
    var options = {
        grid: {
            left: 40,
            top: 20,
            bottom: 40,
            right: 50
        },
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                var res = '<div style="margin-bottom:4px;">' + params[0].name + '</div><div style="margin-bottom:4px;padding-right:6px"><div style="background:' + params[0].color + ';display:inline-block;width:8px;height:8px;margin-right:4px"></div>' +
                    params[0].seriesName + '£º' + params[0].data[1] + (unit ? '%' : '') + '</div><div style="margin-bottom:4px"><div style="background:' + params[1].color + ';display:inline-block;width:8px;height:8px;margin-right:4px"></div>' +
                    params[1].seriesName + '£º' + params[1].data[1] + (unit ? '%' : '') + '</div>';
                if (unit) {
                    res += '<div><div style="background:' + params[2].color + ';display:inline-block;width:4px;height:8px;margin-right:8px"></div>' +
                        params[2].seriesName + '£º' + params[2].data[1] + '%</div>'
                }
                return res
            }
        },
        yAxis: [{
                type: 'value',
                name: 'left',
                splitLine: {
                    lineStyle: {
                        color: '#666'
                    }
                },
                axisLabel: {
                    color: '#666'
                }
            },
            {
                type: 'value',
                name: 'right',
                splitLine: {
                    show: false
                },
                axisLabel: {
                    color: '#666'
                }
            }
        ],
        xAxis: {
            type: 'category',
            /* labels: {
                step: Math.floor(data1.data.length / 8)
            },
            tickWidth: 0 */
            axisLabel: {
                color: '#666'
            }
        },
        legend: {
            show: false
        },
        //每个图表最多是三条曲线，这里可以增加，
        //每个图表的都是类似样式，就是各个图表第一条都是散点，第二条都是折线等，都是相同
        //通过每个图表数据，为空，来对齐想要的样式，
        //就是说此处大量增加每个图表的能容纳的条数。然后每个条是不同的类型，多样话曲线类似
        //然后每个图表使用哪个通过调整数据先后和或用空来代替，跳过某个类型来使用后面的某个类型。
        series: [{
            name: data1.name,
            type: 'line',
            data: data1.data,
            stack: 'data1',
            showAllSymbol: false,
            color: color.lineColor[0]
        }, {
            name: data2.name,
            type: 'scatter',
            data: data2.data,
            stack: 'data2',
            yAxisIndex: 1,
            showAllSymbol: false,
            color: color.lineColor[1]
        }, {
            name: data3.name,
            type: 'line',
            data: data3.data,
            stack: 'data3',
            yAxisIndex: 1,
            showAllSymbol: false,
            color: color.lineColor[2]
        }]
    }
    myChart.setOption(options)
}