a = [
    {
        "text": u'仪表板',
        "name": 'dashboardview',
        "value": 1,
        "parent": 0,
        "showSign": True,
        "items": [{"text": u'只读', "checked": False},
                  {"text": u'读写', "checked": False}]
    },
    {
        "text": '邮件威胁事件',
        "value": 2,
        "parent": 0,
        "showSign": True,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'威胁情报',
        "name": 'mail_threatview',
        "value": 21,
        "parent": 2,
        "showSign": True,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'恶意ddd邮件',
        "name": 'mail_evilview',
        "value": 22,
        "parent": 2,
        "showSign": True,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'垃圾邮件',
        "name": 'mail_spamview',
        "value": 23,
        "parent": 2,
        "showSign": True,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'邮件处置区',
        "value": 3,
        "parent": 0,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'隔离邮件',
        "name": 'deal_isoaview',
        "value": 31,
        "parent": 3,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'卸下武装后放行',
        "name": 'deal_passew',
        "value": 32,
        "parent": 3,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'场景和多维分析',
        "value": 4,
        "parent": 0,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'发件异常',
        "name": 'scene_sendview',
        "value": 41,
        "parent": 4,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'收件异常',
        "name": 'scene_recview',
        "value": 42,
        "parent": 4,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'暴力破解',
        "name": 'scene_crackview',
        "value": 43,
        "parent": 4,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'异常登陆',
        "name": 'scene_abnormalview',
        "value": 44,
        "parent": 4,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'仿冒邮件',
        "name": 'scene_palmview',
        "value": 45,
        "parent": 4,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'邮件多维分析',
        "name": 'scene_dimview',
        "value": 46,
        "parent": 4,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'自定义场景',
        "name": 'scene_customview',
        "value": 47,
        "parent": 4,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'邮件检索',
        "name": 'mail_searchview',
        "value": 5,
        "parent": 0,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": True}]
    }, {
        "text": u'报表管理',
        "value": 6,
        "parent": 0,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'快速报表',
        "name": 'report_taskview',
        "value": 61,
        "parent": 6,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'报表模板',
        "name": 'report_taskview',
        "value": 62,
        "parent": 6,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'系统管理',
        "value": 7,
        "parent": 0,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'系统配置',
        "value": 71,
        "parent": 7,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'基础设置',
        "name": 'config_system_basicview',
        "value": 711,
        "parent": 71,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'配置管理',
        "name": 'config_system_mentview',
        "value": 712,
        "parent": 71,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'升级管理',
        "name": 'config_system_updateview',
        "value": 714,
        "parent": 71,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'安全设置',
        "name": 'config_system_safeview',
        "value": 715,
        "parent": 71,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'存储管理',

        "name": 'config_system_generalview',
        "value": 716,
        "parent": 71,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'系统维护',
        "name": 'config_system_maintview',
        "value": 717,
        "parent": 71,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'策略配置',
        "value": 72,
        "parent": 7,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'邮件处置策略',
        "name": 'config_strategy_mailview',
        "value": 721,
        "parent": 72,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'动态检测策略',
        "name": 'config_strategy_dynamicview',
        "value": 722,
        "parent": 72,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'白名单',
        "name": 'config_strategy_whiteview',
        "value": 723,
        "parent": 72,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    },
    {
        "text": u'加白邮件',
        "name": 'config_strategy_whitedmview',
        "value": 724,
        "parent": 72,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    },
    {
        "text": u'用户管理',
        "value": 73,
        "parent": 7,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'用户hahahah管理',
        "name": 'config_mg_userview',
        "value": 731,
        "parent": 73,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'角色管理',
        "name": 'config_mg_roleview',
        "value": 732,
        "parent": 73,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }, {
        "text": u'审计日志',
        "name": 'config_log_audit',
        "value": 8,
        "parent": 0,
        "items": [{"text": u'只读', "checked": False, "disabled": False},
                  {"text": u'读写', "checked": False, "disabled": False}]
    }
]
