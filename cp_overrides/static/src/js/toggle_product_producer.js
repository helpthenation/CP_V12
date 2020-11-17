odoo.define('cp_overrides.hide', function (require) {
    "use strict";
    var rpc = require('web.rpc');
    var form_renderer = require('web.FormRenderer');
    var FormController = require('web.FormController');

    form_renderer.include({
        _updateView: function ($newContent) {
            var self = this;
            this._super($newContent);
            if(self.state.model === "product.attribute"){
                var $data = this.$el.find('.o_inner_group');
                var dataw = this.$el.find('.o_inner_group');
                var booealan = $(dataw).find('.enable_product_producer input').is(":checked");
                if(booealan == false){
                    $data.each(function () {
                    var headers = $(this).find('thead > tr >.o_column_sortable')
                    var table_data = $(this).find('tbody > tr > .producer')
                        $(headers).each(function(){
                            if(this.innerText === "Producer"){
                                $(this).hide();
                            }
                        });
                        $(table_data).each(function(){
                                $(this).hide();
                        });
                    });
                }
                if(booealan == true){
                    $data.each(function () {
                    var headers = $(this).find('thead > tr >.o_column_sortable')
                    var table_data = $(this).find('tbody > tr > .producer')
                        $(headers).each(function(){
                            if(this.innerText === "Producer"){
                                $(this).show();
                            }
                        });
                        $(table_data).each(function(){
                                $(this).show();
                        });
                    });
                }
            }
        },
       _onClick: function () {
            var self = this;
            this._super();
            if(self.state.model === "product.attribute"){
                var $data = this.$el.find('.o_inner_group');
                var dataw = this.$el.find('.o_inner_group');
                var booealan = $(dataw).find('.enable_product_producer input').is(":checked");
                if(booealan == false){
                    $data.each(function () {
                    var headers = $(this).find('thead > tr >.o_column_sortable')
                    var table_data = $(this).find('tbody > tr > .producer')
                        $(headers).each(function(){
                            if(this.innerText === "Producer"){
                                $(this).hide();
                            }
                        });
                        $(table_data).each(function(){
                                $(this).hide();
                        });
                    });
                }
                if(booealan == true){
                    $data.each(function () {
                    var headers = $(this).find('thead > tr >.o_column_sortable')
                    var table_data = $(this).find('tbody > tr > .producer')
                        $(headers).each(function(){
                            if(this.innerText === "Producer"){
                                $(this).show();
                            }
                        });
                        $(table_data).each(function(){
                                $(this).show();
                        });
                    });
                }
            }
        },
    });

    FormController.include({
        autofocus: function () {
            var result = this._super();
            if (!this.initialState.data.plm_image1){
                $("#li_plm_image1").remove();
                $("#carousel_item_plm_image1").remove();
            }
            if (!this.initialState.data.plm_image2){
                $("#li_plm_image2").remove();
                $("#carousel_item_plm_image2").remove();
            }
            if (!this.initialState.data.plm_image3){
                $("#li_plm_image3").remove();
                $("#carousel_item_plm_image3").remove();
            }
            if (!this.initialState.data.plm_pdf1){
                $("#li_plm_pdf1").remove();
                $("#carousel_item_plm_pdf1").remove();
            }
            if (!this.initialState.data.plm_pdf2){
                $("#li_plm_pdf2").remove();
                $("#carousel_item_plm_pdf2").remove();
            }
            if (!this.initialState.data.plm_pdf3){
                $("#li_plm_pdf3").remove();
                $("#carousel_item_plm_pdf3").remove();
            }
            return result;
        },
    });



});