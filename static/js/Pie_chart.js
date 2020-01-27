


        function postchart() {
            gettime =  new Date().getTime();
            document.getElementById("chart1").innerHTML += '<canvas id="pieChart?gettime=' + gettime + '" style="max-width: 500px; display: inline"></canvas>';

            return false
        };

        function delpostchart() {
           document.getElementById("chart1").innerHTML = null;

           return false
        }




        var flag1 = 0;
        function setFlag1_1() {
            flag1 = 1;

            return flag1
        }


        function setFlag1_2() {
            flag1 = 2;

            return flag1
        }



        function setFlag2_1() {
            flag2 = 1;

            return flag2
        }

        function setFlag2_2() {
            flag2 = 2;

            return flag2
        }

        function setFlag2_3() {
            flag2 = 3;

            return flag2

        }


       //запрос на сервер на получение данных о чарте

         var jlab = [];
         var jdata = [];

         function gochart(){

                areaslct1 = document.getElementById("");
                areaslct2 = document.getElementById("");

                if ((flag1 > 0)&& flag2 > 0){
                    delpostchart();
                    postchart();
                    //$('').load('http://somewhere.com #newContent');
                    //$('#pieChart').toggle();
                    $.ajax({
                        url: "/datareceiver2",
                        type: "POST",
                        success: function(resp){
                            jlab = JSON.parse(resp.dname);
                            jdata = JSON.parse(resp.numb);
                            buildchart();

                            //flag1 = 0;
                            //flag2 = 0;
                            return flag1 && flag2
                        }
                    })

                } else{
                    return false
                }
         }

         // скрипт piechart

          function buildchart() {

              //alert(flag1);
              //alert(flag2);

              var ctxP = document.getElementById('pieChart?gettime=' + gettime).getContext('2d');
              var myPieChart = new Chart(ctxP, {
                  type: 'pie',
                  data: {
                      labels: jlab,
                      datasets: [{
                          data: jdata,
                          backgroundColor: ["#F7464A", "#46BFBD", "#46BFBD"],
                          hoverBackgroundColor: ["#FF5A5E", "#46BFBD", "#46BFBD"]
                      }]
                  },
                  options: {
                      responsive: true
                  }
              });


          }



        function ularsel1() {
            if (document.getElementById('pills-home-tab').selected == 'true') {
                document.getElementById('pills-tab').value = 'product';
                setFlag1();
                buttononclick();
                gochart();
                return false
            }

            else {
                return false
            }
        };


        function buttononclick() {



                var inp3 = document.getElementById('pills-tab').value;
                var inp4 = document.getElementById("pills-tab2").value;


                ctgry = [{"Item 1": inp3, "Item 2": inp4}];

                doWork();

                return false
        }


        //  Отправка данных от браузера (пользовательской страницы) к серверу через ajax (json)

        function doWork() {
            // ajax the JSON to the server
            $.post("/datareceiver", JSON.stringify(ctgry), function(){
            //alert(JSON.stringify(cars))
            });


        }




        $('.dropdown-toggle').dropdown();

      // $(function () {
      //   $('[data-toggle="dropdown"]').dropdown()
      // })



