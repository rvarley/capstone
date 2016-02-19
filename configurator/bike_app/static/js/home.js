
function changeImage(i) {

    var el = document.getElementById("patrick");
    //console.log("value of el at start of fun is: " + el.src);
    urls = ['http://cdn.propelbikes.com/image/cache/data/15-Sahel-Impulse-8-116Ah-Wave-Black-620522256-420x420.jpg',
            'http://cdn.propelbikes.com/image/cache/data/felt-lebowske-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/Victoria/Pedego Interceptor-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/st2blackstep-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/10E_small_freight__77944.1428017663.920.600-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/2015kalkimp-420x420.png',
             'http://cdn.propelbikes.com/image/cache/data/Felt_Bicycles_2016_bruhaul(1)-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/coral12343-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/Victoria/Pedego 26 City White-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/Victoria/Pedego Classic City teal-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/Victoria/Pedego Comfort Coral-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/2015kalkimp-420x420.png',
             'http://cdn.propelbikes.com/image/cache/data/st2standblack-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/felt-sporte-step-thru-420x420.jpg',
             'http://cdn.propelbikes.com/image/cache/data/Victoria/28 Classic City Blue-420x420.jpg'];

    console.log("value of urls.length at start of fun is: " + urls.length);

    if (i <= urls.length){
        el.src = urls[i]
        // el.src = "file///Users/ransomv/capstone/configurator/bike_app/static/images/pdxcg_0" + i + ".jpg')";
    }
    if (i > urls.length) {
        i = 1;
        el.src = urls[i]
    }
    ++i;
    setTimeout(changeImage, 3000, i);
} 