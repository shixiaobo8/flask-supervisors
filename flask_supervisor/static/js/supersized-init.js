{% load staticfiles %}
{% load static %}
jQuery(function($){

    $.supersized({

        // 鍔熻兘
        slide_interval     : 4000,    // 杞崲涔嬮棿鐨勯暱搴�
        transition         : 1,    // 0 - 鏃狅紝1 - 娣″叆娣″嚭锛�2 - 婊戝姩椤讹紝3 - 婊戝姩鍚戝彸锛�4 - 婊戝簳锛�5 - 婊戝潡鍚戝乏锛�6 - 鏃嬭浆鏈ㄩ┈鍙抽敭锛�7 - 宸︽棆杞湪椹�
        transition_speed   : 1000,    // 杞瀷閫熷害
        performance        : 1,    // 0 - 姝ｅ父锛�1 - 娣峰悎閫熷害/璐ㄩ噺锛�2 - 鏇翠紭鐨勫浘鍍忚川閲忥紝涓変紭鐨勮浆鎹㈤€熷害//锛堜粎閫傜敤浜庣伀鐙�/ IE娴忚鍣紝鑰屼笉鏄疻ebkit鐨勶級

        // 澶у皬鍜屼綅缃�
        min_width          : 0,    // 鏈€灏忓厑璁稿搴︼紙浠ュ儚绱犱负鍗曚綅锛�
        min_height         : 0,    // 鏈€灏忓厑璁搁珮搴︼紙浠ュ儚绱犱负鍗曚綅锛�
        vertical_center    : 1,    // 鍨傜洿灞呬腑鑳屾櫙
        horizontal_center  : 1,    // 姘村钩涓績鐨勮儗鏅�
        fit_always         : 0,    // 鍥惧儚缁濅笉浼氳秴杩囨祻瑙堝櫒鐨勫搴︽垨楂樺害锛堝拷鐣ュ垎閽熴€傚昂瀵革級
        fit_portrait       : 1,    // 绾靛悜鍥惧儚灏嗕笉瓒呰繃娴忚鍣ㄩ珮搴�
        fit_landscape      : 0,    // 鏅鐨勫浘鍍忓皢涓嶈秴杩囧搴︾殑娴忚鍣�

        // 缁勪欢
        slide_links        : 'blank',    // 涓埆鐜妭涓烘瘡寮犲够鐏墖锛堥€夐」锛氬亣鐨勶紝'姘�'锛�'鍚�'锛�'绌�'锛�
        slides             : [    // 骞荤伅鐗囧奖鍍�
                                 {image : '{% static "img/1.jpg" %}'},
                                 {image : '{% static "img/2.jpg" %}'},
                                 {image : '{% static "img/3.jpg" %}'}
                       ]

    });)

});