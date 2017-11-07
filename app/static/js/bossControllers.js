/**
 * Created by Administrator on 2015/12/19.
 */


RET_SUCCESS = 0;
RET_FAILED = -1;

var app = angular.module('boss', ['ngRoute', 'ngFileUpload']);

app.config(['$routeProvider', function($routeProvider){
    $routeProvider.when('/AddCatalogue', {
            templateUrl: 'static/templates/addCatalogue.html',
            controller: 'ClgCtrl'
        }).when('/AddCatalogueItem',{
            templateUrl: 'static/templates/addCatalogueItem.html',
            controller: 'ClgCtrl'
        }).when('/AddProduct',{
            templateUrl: 'static/templates/addProduct.html',
            controller: 'ProductCtrl'
        }).otherwise({
            redirectTo: '/AddCatalogue'
        });
}]);


/*
*  clg: catalogue
*
* */
app.service('ClgService',function($http, $rootScope){
    $rootScope.clgSelected = {
        'id': -1,
        'name': null,
        'item': {
             'id': -1,
             'name': null
         }
    };

    this.Init = function(){
        $rootScope.clgSelected.id = -1;
        $rootScope.clgSelected.name = null;
        $rootScope.clgSelected.item.id = -1;
        $rootScope.clgSelected.item.name =null;
    };


    this.GetClgs = function(){
        console.log('GetClgs()');
        return $http.get('/catalogue_list').then(function(response){
            $rootScope.clgs = response.data.catalogue_list;
            return $rootScope.clgs;
        });
    };

     this.AddNewClg = function(newVal){
        console.log('AddNewClg');
        return  $http.post('/add_catalogue',{'catalogue_name': newVal}).then(function(response){
            return response.data;
        });
    };

    this.AddNewClgItem = function(itemName){
        console.log('AddNewClgItem');
        return $http.post('/add_catalogue_item', {'catalogue_item_name': itemName, 'catalogue_id': $rootScope.clgSelected.id}).then(function(response){
            return response.data;
        });
    };

    this.ClgIsActive = function(id){
        if(id == $rootScope.clgSelected.id) return true;
        return false;
    };

    this.SelectClg = function(id){
        console.log('SelectClg()');
        if($rootScope.clgSelected.id != id){
            $rootScope.clgSelected.id = id;
            $rootScope.clgSelected.item.id = -1;
            var clg = this.GetClgById(id);
            if(clg != null){
                console.log($rootScope.clgSelected.name);
                $rootScope.clgSelected.name = clg.name;
            }else{
                 $rootScope.clgSelected.name = null;
            }
        }
    };


    this.SelectClgItem = function(id){
        if($rootScope.clgSelected.item.id != id){
            $rootScope.clgSelected.item.id =id;
            item = this.GetClgItemById(id);
            if(item != null){
                $rootScope.clgSelected.item.name = item.name;
            }else{
                $rootScope.clgSelected.item.name = null;
            }
        }
    };

    this.ClgItemIsActive = function(id){
        if(id == $rootScope.clgSelected.item.id) return true;
        return false;
    };

    this.GetClgItems = function(clgId){
        for( i in $rootScope.clgs){
            console.log('GetClgItems: ', $rootScope.clgs[i].id, ' : ', clgId );
            if($rootScope.clgs[i].id == clgId) return $rootScope.clgs[i].items;
        }
        return null;
    };


    this.GetClgById = function(clgId){
        console.log('GetClgById()');
        console.log($rootScope.clgs);
        for( i in $rootScope.clgs) {
            console.log('GetClgById: ', $rootScope.clgs[i].id, ' : ', clgId );
            if ($rootScope.clgs[i].id == clgId) return $rootScope.clgs[i];
        }
        return null;
    };

    this.GetClgItemById = function(id){
        var items = this.GetClgItems($rootScope.clgSelected.id);
        if(items != null){
            for( i in items) {
                if (items[i].id == id) return items[i];
            }
        }
        return null;
    };

    this.DelClgById = function(id){
        console.log('AddNewClg');
        return  $http.post('/del_catalogue', {'catalogue_id': id}).then(function(response){
            return response.data;
        });
    };

    this.DelClgItemById = function(id){
        console.log('AddNewClg');
        return  $http.post('/del_catalogue_item', {'catalogue_item_id': id}).then(function(response){
            return response.data;
        });
    };

});//ClgService


app.service('AlertService', function($rootScope){

    $rootScope.alerts = [];

    this.AlertMsg = function(type, msg){
        var alert = {};
        alert.type = type;
        alert.msg = msg;
        $rootScope.alerts.push(alert);
    };

    this.Success = function(msg){
        this.AlertMsg('alert-success', msg)
    };

    this.Error = function(msg){
       this.AlertMsg('alert-danger', msg)
    };

    this.DelAlert = function(index){
        $rootScope.alerts.splice(index, 1);
    };

});

app.controller('NavCtrl',function($scope, ClgService){
    /**
     * @return {boolean}
     */
    $scope.ClgHasSelected = function(){
        if(ClgService.ClgIsActive(-1) == true) return false;
        return true;
    };
});


app.controller('AlertCtrl', function($scope, $rootScope, AlertService){

    $scope.GetAlerts = function(){
        return $rootScope.alerts;
    };

    $scope.CloseAlert = function(index){
        AlertService.DelAlert(index);
    };

});


app.controller('ClgCtrl',function($scope, $rootScope, ClgService, AlertService){

    $scope.UpdateClg = function(){
        console.log('UpdateClg');
        ClgService.GetClgs().then(function(clgs){
            console.log('UpdateClg: clgs');
        });
    };

    $scope.SelectClg = function(e){
        id = $(e.target).data('clg-id');
        ClgService.SelectClg(id);
    };

    $scope.ClgIsActive = function(id){
        return ClgService.ClgIsActive(id);
    };

    $scope.ClgItemIsActive = function(id){
        return ClgService.ClgItemIsActive(id);
    };

    $scope.SelectClgItem = function(e){
        id = $(e.target).data('item-id');
        ClgService.SelectClgItem(id);
    };

    $scope.AddNewClg = function(){
        //console.log('AddNewClg');
        if($scope.newVal == null){
            AlertService.Error('Please Input the new catalogue name!')
        }else{
            ClgService.AddNewClg($scope.newVal).then(function(data){
                if(data.ret == RET_SUCCESS ){
                    $scope.UpdateClg();
                    ClgService.Init();
                    AlertService.Success('Success to add new catalogue name: '+$scope.newVal+'!');
                    $scope.newVal = null;
                }else{
                    AlertService.Error('Fail to add new catalogue! Please try it again!');
                }
            });
        }
    };


     $scope.AddNewClgItem = function(){
        //console.log('AddNewClg');
        if($scope.itemName== null){
            AlertService.Error('Please Input the new item name!')
        }else{
            ClgService.AddNewClgItem($scope.itemName).then(function(data){
                if(data.ret == RET_SUCCESS ){
                    AlertService.Success('Success to add new catalogue item name: '+$scope.itemName+' to '+$rootScope.clgSelected.name);
                    $scope.UpdateClg();
                    ClgService.Init();
                    $scope.itemName = null;
                }else{
                    AlertService.Error('Fail to add new catalogue item! Please try it again!');
                }
            });
        }
    };

    $scope.DelClgById = function(id){
        ClgService.DelClgById(id).then(function(data){
            if(data.ret == RET_SUCCESS){
                AlertService.Success('Success to delete catalogue: '+$rootScope.clgSelected.name);
                $scope.UpdateClg();
                ClgService.Init();
            }else{
                AlertService.Error('Fail to delete catalogue: '+$rootScope.clgSelected.name+' , please try it again!');
            }
        });
    };


    $scope.DelClgItemById = function(id){
        ClgService.DelClgItemById(id).then(function(data){
            if(data.ret == RET_SUCCESS){
                AlertService.Success('Success to delete catalogue item: '+$rootScope.clgSelected.item.name);
                $scope.UpdateClg();
                ClgService.Init();
            }else{
                AlertService.Error('Fail to delete catalogue item: '+$rootScope.clgSelected.item.name+' , please try it again!');
            }
        });
    };
});


app.controller('ProductCtrl', function($scope, $rootScope, $http, Upload, ClgService){

    $scope.insertImageSrc = 'http://';
    $scope.editor = new wysihtml5.Editor(document.getElementById('editor'), {
                                    toolbar: document.getElementById('toolbar'),
                                    parserRules:  wysihtml5ParserRules
                                });
    $scope.productImages = [];
    $scope.choosePictures = false;
    $scope.htmlEditorFlag = false;
    $scope.editHtmlBtn = "< / >";
    $scope.allImages = [];
    $scope.images = [];

    $scope.EditHtml = function(){
        if($scope.htmlEditorFlag == false){
            $scope.htmlEditorValue = $scope.GetEditorVal();
            $scope.htmlEditorFlag = true;
        }else{
            $scope.editor.setValue($scope.htmlEditorValue, false);
            $scope.htmlEditorFlag = false;
        }

    };

    $scope.SelectClg = function(id){
        clg = ClgService.GetClgById(id);
        if(clg != null){
             $rootScope.clgSelected.id = id;
             $rootScope.clgSelected.name = clg.name;
             $scope.items = clg.items;
             console.log("SelectClg() > Items: ", clg.items);
        }else{
            ClgService.Init();
        }
    };

    $scope.SelectClgItem = function(id){
        item = ClgService.GetClgItemById(id);
        if(item != null){
            $rootScope.clgSelected.item.id = id;
            $rootScope.clgSelected.item.name = item.name;
            console.log('ClgItem: ',item.id,'(',item.name,')');
        }else{
            $rootScope.clgSelected.item.id = -1;
            $rootScope.clgSelected.item.name =null;
        }
    };


    $scope.ChoosePictures = function(){
        $scope.choosePictures = !$scope.choosePictures;
    };

    $scope.ClickImage = function(image){
        for(var i=0; i < $scope.productImages.length; i++){
            if($scope.productImages[i].id == image.id){
                $scope.productImages.splice(i,1);
                return 0;
            }
        }
        $scope.productImages.push(image);
    };

    $scope.UpdateClg = function(){
        ClgService.GetClgs().then(function(clgs){
            console.log('UpdateClg()')
        });
    };

    $scope.UploadFile = function(file){
        Upload.upload({
            url: '/upload_product_image',
            data: {file: file}
        }).then(function(resp){
            console.log('Success file upload');
            $scope.UpdateImages(true);
        });
    };

    $scope.InitDisplayImages = function(size){
        $scope.images = [];
        for(var i = 0; i < $scope.allImages.length && i < size; i+=1){
            $scope.images.push($scope.allImages[i]);
        }
    };

    $scope.ShowMoreImages = function(){
         if($scope.images.length == $scope.allImages.length){
             alert("No More Images!");
             return 0;
         }
         var size = $scope.images.length + 2;
         for(var i = size - 2; i < $scope.allImages.length &&  i < size; i+=1){
            $scope.images.push($scope.allImages[i]);
        }
    };

    //flag : false means just init
    //flag: true means upload new image
    $scope.UpdateImages = function(flag){
        if(flag == true || $scope.allImages.length == 0){
            $http.get('/get_product_images').then(function(response){
                $scope.allImages = response.data.images;
                console.log("updateImages: ",$scope.images.length);
                $scope.InitDisplayImages($scope.images.length + 1);
            });
        }
    };


    $scope.SelectImage = function(src){
        $scope.insertImageSrc = src;
        console.log($scope.insertImageSrc);
    };

    $scope.FormatDate = function(date){
        var year = date.getFullYear();
        var month = date.getMonth()+1 <10 ? '0'+(date.getMonth()+1) : date.getMonth()+1;
        var day = date.getDate() < 10 ? '0'+date.getDate() : date.getDate();
        return  year+'-'+month+'-'+day;
    };

    $scope.ValidateInput = function(){
        //date
        if($scope.date == null || $rootScope.clgSelected.item.id < 0 || $scope.productImages.length == 0)
            return false;
    };

    $scope.FormValue = function(){
        var data = {};
        data.date = $scope.FormatDate($scope.date);
        data.title = $scope.title;
        data.keywords = $scope.keywords;
        data.partno = $scope.partno;
        data.power = $scope.power;
        data.voltage = $scope.voltage;
        data.introduction = $scope.introduction;
        data.description = $scope.GetEditorVal();
        data.image_ids = [];
        data.catalogue_item_id = $rootScope.clgSelected.item.id;
        for(var i = 0; i < $scope.productImages.length; i++){
           data.image_ids.push($scope.productImages[i].id);
        }
        console.log(data);
        return data;
    };

    $scope.GetEditorVal = function(){
        //console.log($scope.FormatDate($scope.date));
        //console.log($scope.editor.getValue(false));
        return $scope.editor.getValue(false);
    };

    $scope.Submit = function(){
        if($scope.ValidateInput() == false){
            alert("请完善数据！");
        }else{
            data = $scope.FormValue();
            return  $http.post('/add_product', data).then(function(response){
                return response.data;
            }).then(function(data){
                 if(data.ret == RET_SUCCESS){
                     alert("添加产品成功: ",$rootScope.clgSelected.name," -> ",$rootScope.clgSelected.item.name,"！");
                 }
            });
        }
    }
});


app.controller('CaseCtrl', function($scope, $rootScope, $http, Upload){

    $scope.insertImageSrc = 'http://';
    $scope.editor = new wysihtml5.Editor(document.getElementById('editor'), {
                                    toolbar: document.getElementById('toolbar'),
                                    parserRules:  wysihtml5ParserRules
                                });
    $scope.caseImages = [];
    $scope.choosePictures = false;
    $scope.htmlEditorFlag = false;
    $scope.editHtmlBtn = "< / >";
    $scope.allImages = [];
    $scope.images = [];

    $scope.EditHtml = function(){
        if($scope.htmlEditorFlag == false){
            $scope.htmlEditorValue = $scope.GetEditorVal();
            $scope.htmlEditorFlag = true;
        }else{
            $scope.editor.setValue($scope.htmlEditorValue, false);
            $scope.htmlEditorFlag = false;
        }

    };


    $scope.ChoosePictures = function(){
        $scope.choosePictures = !$scope.choosePictures;
    };

    $scope.ClickImage = function(image){
        for(var i=0; i < $scope.caseImages.length; i++){
            if($scope.caseImages[i].id == image.id){
                $scope.caseImages.splice(i,1);
                return 0;
            }
        }
        $scope.caseImages.push(image);
    };

    $scope.UploadFile = function(file){
        Upload.upload({
            url: '/upload_case_image',
            data: {file: file}
        }).then(function(resp){
            console.log('Success file upload');
            $scope.UpdateImages(true);
        });
    };

    $scope.InitDisplayImages = function(size){
        $scope.images = [];
        for(var i = 0; i < $scope.allImages.length && i < size; i+=1){
            $scope.images.push($scope.allImages[i]);
        }
    };

    $scope.ShowMoreImages = function(){
         if($scope.images.length == $scope.allImages.length){
             alert("No More Images!");
             return 0;
         }
         var size = $scope.images.length + 2;
         for(var i = size - 2; i < $scope.allImages.length &&  i < size; i+=1){
            $scope.images.push($scope.allImages[i]);
        }
    };

    //flag : false means just init
    //flag: true means upload new image
    $scope.UpdateImages = function(flag){
        if(flag == true || $scope.allImages.length == 0){
            $http.get('/get_case_images').then(function(response){
                $scope.allImages = response.data.images;
                console.log("updateImages: ",$scope.images.length);
                $scope.InitDisplayImages($scope.images.length + 1);
            });
        }
    };


    $scope.SelectImage = function(src){
        $scope.insertImageSrc = src;
        console.log($scope.insertImageSrc);
    };

    $scope.FormatDate = function(date){
        var year = date.getFullYear();
        var month = date.getMonth()+1 <10 ? '0'+(date.getMonth()+1) : date.getMonth()+1;
        var day = date.getDate() < 10 ? '0'+date.getDate() : date.getDate();
        return  year+'-'+month+'-'+day;
    };

    $scope.ValidateInput = function(){
        //date
        if($scope.date == null || $scope.caseImages.length == 0)
            return false;
    };

    $scope.FormValue = function(){
        var data = {};
        data.date = $scope.FormatDate($scope.date);
        data.title = $scope.title;
        data.keywords = $scope.keywords;
        data.introduction = $scope.introduction;
        data.description = $scope.GetEditorVal();
        data.image_ids = [];
        for(var i = 0; i < $scope.caseImages.length; i++){
           data.image_ids.push($scope.caseImages[i].id);
        }
        console.log(data);
        return data;
    };

    $scope.GetEditorVal = function(){
        //console.log($scope.FormatDate($scope.date));
        //console.log($scope.editor.getValue(false));
        return $scope.editor.getValue(false);
    };

    $scope.Submit = function(){
        if($scope.ValidateInput() == false){
            alert("请完善数据！");
        }else{
            data = $scope.FormValue();
            return  $http.post('/add_case', data).then(function(response){
                return response.data;
            }).then(function(data){
                 if(data.ret == RET_SUCCESS){
                     alert("添加案例成功！");
                 }else{
                     alert("添加案例失败！");
                 }
            });
        }
    }
});


app.controller('NewsCtrl', function($scope, $rootScope, $http, Upload){

    $scope.insertImageSrc = 'http://';
    $scope.editor = new wysihtml5.Editor(document.getElementById('editor'), {
                                    toolbar: document.getElementById('toolbar'),
                                    parserRules:  wysihtml5ParserRules
                                });
    $scope.newsImages = [];
    $scope.choosePictures = false;
    $scope.htmlEditorFlag = false;
    $scope.editHtmlBtn = "< / >";
    $scope.allImages = [];
    $scope.images = [];

    $scope.EditHtml = function(){
        if($scope.htmlEditorFlag == false){
            $scope.htmlEditorValue = $scope.GetEditorVal();
            $scope.htmlEditorFlag = true;
        }else{
            $scope.editor.setValue($scope.htmlEditorValue, false);
            $scope.htmlEditorFlag = false;
        }

    };


    $scope.ChoosePictures = function(){
        $scope.choosePictures = !$scope.choosePictures;
    };

    $scope.ClickImage = function(image){
        for(var i=0; i < $scope.newsImages.length; i++){
            if($scope.newsImages[i].id == image.id){
                $scope.newsImages.splice(i,1);
                return 0;
            }
        }
        $scope.newsImages.push(image);
    };

    $scope.UploadFile = function(file){
        Upload.upload({
            url: '/upload_news_image',
            data: {file: file}
        }).then(function(resp){
            console.log('Success file upload');
            $scope.UpdateImages(true);
        });
    };

    $scope.InitDisplayImages = function(size){
        $scope.images = [];
        for(var i = 0; i < $scope.allImages.length && i < size; i+=1){
            $scope.images.push($scope.allImages[i]);
        }
    };

    $scope.ShowMoreImages = function(){
         if($scope.images.length == $scope.allImages.length){
             alert("No More Images!");
             return 0;
         }
         var size = $scope.images.length + 2;
         for(var i = size - 2; i < $scope.allImages.length &&  i < size; i+=1){
            $scope.images.push($scope.allImages[i]);
        }
    };

    //flag : false means just init
    //flag: true means upload new image
    $scope.UpdateImages = function(flag){
        if(flag == true || $scope.allImages.length == 0){
            $http.get('/get_news_images').then(function(response){
                $scope.allImages = response.data.images;
                console.log("updateImages: ",$scope.images.length);
                $scope.InitDisplayImages($scope.images.length + 1);
            });
        }
    };


    $scope.SelectImage = function(src){
        $scope.insertImageSrc = src;
        console.log($scope.insertImageSrc);
    };

    $scope.FormatDate = function(date){
        var year = date.getFullYear();
        var month = date.getMonth()+1 <10 ? '0'+(date.getMonth()+1) : date.getMonth()+1;
        var day = date.getDate() < 10 ? '0'+date.getDate() : date.getDate();
        return  year+'-'+month+'-'+day;
    };

    $scope.ValidateInput = function(){
        //date
        if($scope.date == null)
            return false;
    };

    $scope.FormValue = function(){
        var data = {};
        data.date = $scope.FormatDate($scope.date);
        data.title = $scope.title;
        data.keywords = $scope.keywords;
        data.introduction = $scope.introduction;
        data.description = $scope.GetEditorVal();
        //data.image_ids = [];
        //for(var i = 0; i < $scope.newsImages.length; i++){
          // data.image_ids.push($scope.newsImages[i].id);
        //}
        console.log(data);
        return data;
    };

    $scope.GetEditorVal = function(){
        //console.log($scope.FormatDate($scope.date));
        //console.log($scope.editor.getValue(false));
        return $scope.editor.getValue(false);
    };

    $scope.Submit = function(){
        if($scope.ValidateInput() == false){
            alert("请完善数据！");
        }else{
            data = $scope.FormValue();
            return  $http.post('/add_news', data).then(function(response){
                return response.data;
            }).then(function(data){
                 if(data.ret == RET_SUCCESS){
                     alert("添加News成功！");
                 }else{
                     alert("添加News失败！");
                 }
            });
        }
    }
});



