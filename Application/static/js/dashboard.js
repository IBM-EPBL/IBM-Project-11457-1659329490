function load_payers_chart(data){
    var myChart = echarts.init(document.getElementById('payers-chart'));
    var option = {
        tooltip: {},
        legend: {}, 
        dataset:{
            source: data
        },
        series: [
            {
                name: 'Payer',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                
                borderColor: '#fff',
                borderWidth: 2
                },
                label: {
                show: false,
                },
                labelLine: {
                show: false
                }, 
            }
            ]
    };

    myChart.setOption(option);

}


function load_category_trend(data){
    var myChart = echarts.init(document.getElementById('spendings-chart'));
    option = {
        legend: {},
        
        xAxis: {
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        yAxis: {
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          },
          scale: true
        },
        series: data.map((d) => {  
            return {
              name: d['name'],
              data: [d['series']],
              type: 'scatter',
              symbolSize: function (data) {
                return data[2];
              },
              emphasis: {
                focus: 'series',
                label: {
                  show: true,
                  formatter: function (param){ 
                    return param.data[3];
                  },
                  position: 'top'
                }
              },
              encode:{
                x: 0,
                y:1
              }
            
            }
        
        })
      };

      myChart.setOption(option);
}

function load_monthly_chart(data){
    var myChart = echarts.init(document.getElementById('monthly-chart'));
    var option = {
        tooltip: {},
        legend: {}, 
        dataset:{
            source: data
        },
        xAxis: {
            type: 'category',
            
          },
          yAxis: {},
          series: {
            type: 'bar',
            encode: { x: 'name', y: 'amount' },

          }
    };

    myChart.setOption(option);
}

function load_weekly_chart(data){
    var myChart = echarts.init(document.getElementById(`weekly-chart`));
        var option = {
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross',
                label: {
                  backgroundColor: '#6a7985'
                }
              }
            },
            legend: {},
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            dataset:{
              source: data
            },
            xAxis: [
              {
                type: 'category',
                
              }
            ],
            yAxis: [
              {
                type: 'value'
              }
            ],
            series: [
              {
                type: 'line',
                stack: 'Total',
                areaStyle: {},
                
                encode:{
                  x: 0,
                  y: 1
                }
              },
            ]
          };

        myChart.setOption(option);
}

function load_budget_chart(data){
    for (let d of data){
        var myChart = echarts.init(document.getElementById(`budget-${d['id']}`));
        var option = {
            tooltip: {},
           
            dataset:{
                source: d['categories']
            },
            series: [
                {
                  name: d['name'],
                  type: 'pie',
                  radius: ['40%', '70%'],
                  avoidLabelOverlap: false,
                  itemStyle: {
                    
                    borderColor: '#fff',
                    borderWidth: 2
                  },
                  label: {
                    show: false,
                  },
                  labelLine: {
                    show: false
                  }, 
                }
              ]
        };

        myChart.setOption(option);
    }
}