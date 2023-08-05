from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/management-security.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_management_security = resolve('management_security')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_3((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security)):
        pass
        yield '\n## Management Security\n\n### Management Security Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
        if t_3(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'entropy_source')):
            pass
            yield '| Entropy source | '
            yield str(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'entropy_source'))
            yield ' |\n'
        if t_3(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'encryption_key_common')):
            pass
            yield '| Common password encryption key | '
            yield str(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'encryption_key_common'))
            yield ' |\n'
        if t_3(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'encryption_reversible')):
            pass
            yield '| Reversible password encryption | '
            yield str(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'encryption_reversible'))
            yield ' |\n'
        if t_3(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'minimum_length')):
            pass
            yield '| Minimum password length | '
            yield str(environment.getattr(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'password'), 'minimum_length'))
            yield ' |\n'
        if t_3(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'ssl_profiles')):
            pass
            yield '\n### Management Security SSL Profiles\n\n| SSL Profile Name | TLS protocol accepted | Certificate filename | Key filename | Cipher List |\n| ---------------- | --------------------- | -------------------- | ------------ | ----------- |\n'
            for l_1_ssl_profile in t_2(environment.getattr((undefined(name='management_security') if l_0_management_security is missing else l_0_management_security), 'ssl_profiles')):
                _loop_vars = {}
                pass
                yield '| '
                yield str(t_1(environment.getattr(l_1_ssl_profile, 'name'), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(l_1_ssl_profile, 'tls_versions'), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(environment.getattr(l_1_ssl_profile, 'certificate'), 'file'), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(environment.getattr(l_1_ssl_profile, 'certificate'), 'key'), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(l_1_ssl_profile, 'cipher_list'), '-'))
                yield ' |\n'
            l_1_ssl_profile = missing
        yield '\n### Management Security Configuration\n\n```eos\n'
        template = environment.get_template('eos/management-security.j2', 'documentation/management-security.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '2=30&10=33&11=36&13=38&14=41&16=43&17=46&19=48&20=51&22=53&28=56&29=60&36=72'