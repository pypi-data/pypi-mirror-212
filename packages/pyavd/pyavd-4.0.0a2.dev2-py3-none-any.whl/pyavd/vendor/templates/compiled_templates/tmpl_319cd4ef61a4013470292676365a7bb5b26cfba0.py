from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/qos-profiles.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_qos_profiles = resolve('qos_profiles')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    for l_1_profile in t_1((undefined(name='qos_profiles') if l_0_qos_profiles is missing else l_0_qos_profiles), 'name'):
        _loop_vars = {}
        pass
        yield '!\nqos profile '
        yield str(environment.getattr(l_1_profile, 'name'))
        yield '\n'
        if t_2(environment.getattr(l_1_profile, 'trust')):
            pass
            if (environment.getattr(l_1_profile, 'trust') == 'disabled'):
                pass
                yield '   no qos trust\n'
            else:
                pass
                yield '   qos trust '
                yield str(environment.getattr(l_1_profile, 'trust'))
                yield '\n'
        if t_2(environment.getattr(l_1_profile, 'cos')):
            pass
            yield '   qos cos '
            yield str(environment.getattr(l_1_profile, 'cos'))
            yield '\n'
        if t_2(environment.getattr(l_1_profile, 'dscp')):
            pass
            yield '   qos dscp '
            yield str(environment.getattr(l_1_profile, 'dscp'))
            yield '\n'
        if t_2(environment.getattr(environment.getattr(l_1_profile, 'shape'), 'rate')):
            pass
            yield '   shape rate '
            yield str(environment.getattr(environment.getattr(l_1_profile, 'shape'), 'rate'))
            yield '\n'
        if t_2(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'service_policy'), 'type'), 'qos_input')):
            pass
            yield '   service-policy type qos input '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'service_policy'), 'type'), 'qos_input'))
            yield '\n'
        for l_2_tx_queue in t_1(environment.getattr(l_1_profile, 'tx_queues'), 'id'):
            _loop_vars = {}
            pass
            yield '   !\n   tx-queue '
            yield str(environment.getattr(l_2_tx_queue, 'id'))
            yield '\n'
            if t_2(environment.getattr(l_2_tx_queue, 'bandwidth_percent')):
                pass
                yield '      bandwidth percent '
                yield str(environment.getattr(l_2_tx_queue, 'bandwidth_percent'))
                yield '\n'
            elif t_2(environment.getattr(l_2_tx_queue, 'bandwidth_guaranteed_percent')):
                pass
                yield '      bandwidth guaranteed percent '
                yield str(environment.getattr(l_2_tx_queue, 'bandwidth_guaranteed_percent'))
                yield '\n'
            if t_2(environment.getattr(l_2_tx_queue, 'priority')):
                pass
                yield '      '
                yield str(environment.getattr(l_2_tx_queue, 'priority'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(l_2_tx_queue, 'shape'), 'rate')):
                pass
                yield '      shape rate '
                yield str(environment.getattr(environment.getattr(l_2_tx_queue, 'shape'), 'rate'))
                yield '\n'
        l_2_tx_queue = missing
        for l_2_uc_tx_queue in t_1(environment.getattr(l_1_profile, 'uc_tx_queues'), 'id'):
            _loop_vars = {}
            pass
            yield '   !\n   uc-tx-queue '
            yield str(environment.getattr(l_2_uc_tx_queue, 'id'))
            yield '\n'
            if t_2(environment.getattr(l_2_uc_tx_queue, 'bandwidth_percent')):
                pass
                yield '      bandwidth percent '
                yield str(environment.getattr(l_2_uc_tx_queue, 'bandwidth_percent'))
                yield '\n'
            elif t_2(environment.getattr(l_2_uc_tx_queue, 'bandwidth_guaranteed_percent')):
                pass
                yield '      bandwidth guaranteed percent '
                yield str(environment.getattr(l_2_uc_tx_queue, 'bandwidth_guaranteed_percent'))
                yield '\n'
            if t_2(environment.getattr(l_2_uc_tx_queue, 'priority')):
                pass
                yield '      '
                yield str(environment.getattr(l_2_uc_tx_queue, 'priority'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(l_2_uc_tx_queue, 'shape'), 'rate')):
                pass
                yield '      shape rate '
                yield str(environment.getattr(environment.getattr(l_2_uc_tx_queue, 'shape'), 'rate'))
                yield '\n'
        l_2_uc_tx_queue = missing
        for l_2_mc_tx_queue in t_1(environment.getattr(l_1_profile, 'mc_tx_queues'), 'id'):
            _loop_vars = {}
            pass
            yield '   !\n   mc-tx-queue '
            yield str(environment.getattr(l_2_mc_tx_queue, 'id'))
            yield '\n'
            if t_2(environment.getattr(l_2_mc_tx_queue, 'bandwidth_percent')):
                pass
                yield '      bandwidth percent '
                yield str(environment.getattr(l_2_mc_tx_queue, 'bandwidth_percent'))
                yield '\n'
            elif t_2(environment.getattr(l_2_mc_tx_queue, 'bandwidth_guaranteed_percent')):
                pass
                yield '      bandwidth guaranteed percent '
                yield str(environment.getattr(l_2_mc_tx_queue, 'bandwidth_guaranteed_percent'))
                yield '\n'
            if t_2(environment.getattr(l_2_mc_tx_queue, 'priority')):
                pass
                yield '      '
                yield str(environment.getattr(l_2_mc_tx_queue, 'priority'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(l_2_mc_tx_queue, 'shape'), 'rate')):
                pass
                yield '      shape rate '
                yield str(environment.getattr(environment.getattr(l_2_mc_tx_queue, 'shape'), 'rate'))
                yield '\n'
        l_2_mc_tx_queue = missing
    l_1_profile = missing

blocks = {}
debug_info = '2=24&4=28&5=30&6=32&9=38&12=40&13=43&15=45&16=48&18=50&19=53&21=55&22=58&24=60&26=64&27=66&28=69&29=71&30=74&32=76&33=79&35=81&36=84&39=87&41=91&42=93&43=96&44=98&45=101&47=103&48=106&50=108&51=111&54=114&56=118&57=120&58=123&59=125&60=128&62=130&63=133&65=135&66=138'