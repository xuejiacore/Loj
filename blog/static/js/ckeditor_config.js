/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */
CKEDITOR.editorConfig = function (config) {
    // 设置宽高
    config.height = 400;
    config.autosave = false;

    //  屏蔽换行符<br>
    config.enterMode = CKEDITOR.ENTER_BR;
    // 屏蔽段落<p>
    config.shiftEnterMode = CKEDITOR.ENTER_P;
    config.extraPlugins = 'customace';
};
