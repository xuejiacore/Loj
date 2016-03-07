/**
 * Created by xuejia on 2016/2/23.
 */
/**
 * Created by xuejia on 2016/2/23.
 */
CKEDITOR.editorConfig = function (config) {
    // 设置宽高
    config.height = 100;
    config.width = 600;
    config.autosave = false;
    // 拖拽改变尺寸
    config.resize_enabled = false;
    // 移除地步栏插件
    config.removePlugins = 'elementspath';
    //  屏蔽换行符<br>
    config.enterMode = CKEDITOR.ENTER_BR;
    // 屏蔽段落<p>
    config.shiftEnterMode = CKEDITOR.ENTER_P;

    config.toolbarGroups = [
        {name: 'document', groups: ['mode', 'document', 'doctools']},
        {name: 'clipboard', groups: ['clipboard', 'undo']},
        {name: 'editing', groups: ['find', 'selection', 'spellchecker', 'editing']},
        '/',
        {name: 'basicstyles', groups: ['basicstyles', 'cleanup']},
        {name: 'paragraph', groups: ['list', 'indent', 'blocks', 'align', 'bidi', 'paragraph']},
        {name: 'forms', groups: ['forms']},
        {name: 'links', groups: ['links']},
        {name: 'insert', groups: ['insert']},
        {name: 'styles', groups: ['styles']},
        {name: 'colors', groups: ['colors']},
        {name: 'tools', groups: ['tools']},
        '/',
        {name: 'others', groups: ['others']},
        {name: 'about', groups: ['about']}
    ];

    config.removeButtons = 'Cut,Copy,Paste,PasteText,PasteFromWord,Redo,Undo,Find,Replace,SelectAll,Scayt,Form,Checkbox,Radio,TextField,Textarea,Select,Button,HiddenField,Templates,NewPage,Save,Preview,Print,Source,Subscript,Superscript,RemoveFormat,CreateDiv,BidiRtl,BidiLtr,Language,Anchor,Flash,Smiley,SpecialChar,PageBreak,Iframe,Maximize,About,JustifyCenter,JustifyLeft,JustifyRight,JustifyBlock,Blockquote,Styles,Format,Table,HorizontalRule,ShowBlocks';
};
