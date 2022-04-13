/* Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('website_mega_menus.website_mega_menus', function(require) {
    "use strict";
    var base = require('web_editor.base');
    var ajax = require('web.ajax');
    var sAnimation = require('website.content.snippets.animation');
    sAnimation.registry.affixMenu = sAnimation.registry.affixMenu.extend({
        _onWindowUpdate: function() {
            // var wOffset = $(window).scrollTop();
            // var hOffset = this.$target.scrollTop();
            var wOffset = $(window).scrollTop();
            var hOffset = this.$target.scrollTop();
            let width = window.innerWidth;
            if (width > 767) {
                $('header').removeClass('mobile-header-active');
                $('#top_menu >li .dropdown-content').css('display', "");
                this.$headerClone.toggleClass('affixed', wOffset > (hOffset + 300));
            } else {
                let selector = $('.o_affix_enabled #top_menu_collapse');
                let menu = document.querySelector('.o_affix_enabled');
                let cond = true;
                if (selector.hasClass('show') && menu.offsetHeight >= $(document).scrollTop()) {
                    cond = false;
                }
                if (cond === true) {
                    var dom_ele = $('header #top_menu_collapse');
                    let check = dom_ele.hasClass('show');
                    dom_ele.removeClass('show');
                    if (check) {
                        window.scrollTo(0, $(document).scrollTop() - document.querySelector('#top_menu_collapse').offsetHeight);
                    }
                    if (wOffset > (hOffset + 300) == false) {
                        $('header #top_menu_collapse_clone').removeClass('show');
                    }
                    this.$headerClone.toggleClass('affixed', wOffset > (hOffset + 300));
                }
            }
        },
    });

    $(document).on('click', '.mega-menu-link', function(ev) {
        ev.preventDefault();
        let width = window.innerWidth;
        if (width > 767) {
            window.location.href = $(this).attr("mega_menu_url");
        } else {
            var ref = $(this).parent('li').find('.dropdown-content');
            $('#top_menu li .dropdown-content').css('display', 'none');
            if (ref.length > 0) {
                ref.toggle();
            }
        }
    });

    $(document).click(function() {
        $('#fly_out_view').hide();
    });

    function fly_out_view_open(e) {
        e.stopPropagation();
        $('#fly_out_view').show();
    }

    $(document).on('click', '#top_menu  .dropdown-content .header span', function(ev) {
        $(this).parents('.dropdown-content').css('display', 'none');
    })

    $(document).ready(function() {
        $(".hover_mega_menu").parents('li.nav-item:not(.wk_dropdown)').addClass("super")
            .find('>.dropdown-menu >.wk_dropdown >.mega-menu-link').addClass('mega_child');
        $(document)
            .on('click', '#fly_out_view_open, #fly_out_view .dropdown-menu', fly_out_view_open)
            .on('hover', '#fly_out_view_open, #fly_out_view .dropdown-menu', function(e) {
                var width = window.innerWidth;
                if (width > 767) {
                    fly_out_view_open(e);
                }
            });
        $('#fly_out_view').on('click', function(e) {
            $('#fly_out_view').show();
            console.log("fdfdf");
            e.stopPropagation();

        })

        set_selected_menu();

        $('.levelclass').each(function(index) {
            var level = $(this).attr('level')
            $(this).css({
                'padding-left': 6 * level + '%'
            })
        });

        $("#top_menu .dropdown").hover(function() {
            var color = $(this).find('.dropbtn').attr('color')
            var mega_menu = $(this).find('.dropbtn').attr('mega_menu')
            var width = window.innerWidth;
            if (mega_menu == 'True' && width > 767) {
                $(this).find('.mega-menu-link').css({
                    'border-bottom': '5px solid #' + color + '',
                    'padding-bottom': '8px'
                })
            }
        }, function() {
            $(this).find('.mega-menu-link').css({
                'border-bottom': '5px solid transparent'
            })
        });

        $('main').click(function() {
            $(".navbar-collapse").collapse('hide');
        })

        $('#fly_out_view .fa-times').click(function(e) {
            $("#fly_out_view").hide();
            e.stopPropagation();
        })

        $('#top_menu li .dropdown-content').children().find('a').click(function(e) {
            localStorage.setItem('default_menu_bar', $(this).parents('li').last().prop('id'));
        })

    });

    $(document).on('click', '.mega_child', function(ev) {
        console.log("dfffdfd");
        var width = window.innerWidth;
        if (width < 768) {
            $('#top_menu').find('.dropdown-content').hide();
            $(this).parent('li').find('.dropdown-content').show();
            ev.stopPropagation();
        }
    })

    function set_selected_menu() {
        try {
            var bool = true;
            $('#top_menu li').each(function() {
                if ($(this).prop('class').includes('active')) {
                    localStorage.setItem('default_menu_bar', '')
                    bool = false;
                }
            });
            if (bool === true && window.location.href.includes('/shop/category/')) {
                let ref = '#' + localStorage.getItem('default_menu_bar');
                $(ref).addClass('active');
            }
        } catch (e) {}

    }

});
