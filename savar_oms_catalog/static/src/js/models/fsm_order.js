odoo.define('savar_oms_catalog.model_fsm_order', function (require) {
    'use strict';

    var Class = require('web.Class');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var _t = core._t;

    var Button_XLS = Class.extend({
        init: function () {
            var self = this;
            $(document).ready(function(event)
            {
                
                $('.xls_importer').unbind('click');
                $('.xls_importer').off('click');
                $(document).on('click', '.xls_importer', function(event)
                {
                    if($(".modal-body").length==0)
                    {
                        var rendered_html = QWeb.render('xls_importer');
                    Dialog.alert(self, '',
                        {
                            $content: $("<div/>").html(rendered_html,{'csrf_token':core.csrf_token, 'url_redirection': window.location.href}),
                            title: _t('Importador de Ordenes de Trabajo'),
                            buttons:[]
                        });

                    self.update_xlsx_templates_board();

                    var inteval = setInterval(function(){
                        var count = $("input[name='url_redirection']").length;
                        if(count>0)
                        {
                            $("input[name='url_redirection']").val(window.location.href);
                            clearInterval(inteval);
                        }

                    });  
                    }                                      

                });
                var interval = setInterval(function()
                {
                    if($('div[name=stage_id] button').length>0)
                    {
                        $('div[name=stage_id] button').each(function(index, _button){
                            $(_button).on('click',function()
                            {
                                self.update_stage($(this));
                            });
                            $(_button).addClass('stage_id');
                        });

                        $('button.stage_id').off('click');
                        $(document).on('click', 'button.stage_id', function(event)
                        {
                            self.update_stage($(this));
                        });
                        clearInterval(interval);
                    }
                },2);

                var interval = setInterval(function()
                    {
                        if( $('div.diplayer-control-fields').length > 0 )
                        {
                            
                            $('div.diplayer-control-fields').unbind('click');
                            $('div.diplayer-control-fields').off('click');
                            $('div.diplayer-control-fields').on('click', function(event)
                            {
                                if( $('div.board-xlsx-templates-fields').hasClass('important-hidden') )
                                {
                                    $('div.board-xlsx-templates-fields').removeClass('important-hidden');
                                    $('div.board-xlsx-templates-fields').removeClass('diplayer-control-fields');
                                }
                                else
                                {
                                    $('div.board-xlsx-templates-fields').addClass('important-hidden');
                                    $('div.board-xlsx-templates-fields').addClass('diplayer-control-fields');
                                }
                            });                            

                            clearInterval(interval);

                        }                        
                    }, 5);

                    var inteval_001 = setInterval(function(){
                        var count = $(".modal-body").length;
                        if(count>1)
                        {
                            $(".o_technical_modal").first().remove();
                            clearInterval(inteval_001);
                        }
                    }); 
            });            

        },
        update_xlsx_templates_board: function()
        {
            var self = this;
            var _args = {};
            rpc.query({
                model: "xlsx.templates",
                method: "get_templates",
                args: ["", _args],
            }).then((xlsx_templates,) =>
            {                        
                if(xlsx_templates)
                {  
                    var rendered_html = QWeb.render('xls_templates_buttons', {'xlsx_templates':xlsx_templates});
                    $('.board-xlsx-templates').html(rendered_html);

                    var interval = setInterval(function()
                    {
                        if( $('div.btn-downloadxlsx').length > 0 )
                        {
                            $('div.btn-downloadxlsx').on('click', function(event)
                            {
                                
                                event.preventDefault();
                                var id_xlsx = $(this).attr('id');

                                var _args = { 'id_xlsx': id_xlsx };
                                rpc.query({
                                    model: "xlsx.templates",
                                    method: "download_template",
                                    args: ["", _args],
                                }).then((xlsx_template,) =>
                                {
                                    if(xlsx_template)
                                    {
                                        var _url = xlsx_template.url;
                                        window.open(_url, "Plantilla XLSX para Ordenes de Trabajo");
                                        self.update_xlsx_templates_board();
                                    }
                                });
                                
                            });                          

                            clearInterval(interval);
                            
                            $('div.diplayer-control-fields').unbind('click');
                            $('div.diplayer-control-fields').off('click');
                            $('div.diplayer-control-fields').on('click', function(event)
                            {
                                
                                if( $('div.board-xlsx-templates-fields').hasClass('important-hidden') )
                                {
                                    $('div.board-xlsx-templates-fields').removeClass('important-hidden');
                                    $('div.board-xlsx-templates-fields').removeClass('diplayer-control-fields');
                                }
                                else
                                {
                                    $('div.board-xlsx-templates-fields').addClass('important-hidden');
                                    $('div.board-xlsx-templates-fields').addClass('diplayer-control-fields');
                                }
                            });

                        }                        
                    }, 5);                    

                }
            });
        },
        update_stage: function(selector)
        {
            /*var stage_id = selector.attr('data-value');
            var _params = {'stage_id': stage_id};
            return rpc.query({
                model: "fsm.order",
                method: "update_stage",
                args: ["", _params],
            }).then(() =>
            {
            });*/
        },        
    });
    var button = new Button_XLS();
    button.init()
});