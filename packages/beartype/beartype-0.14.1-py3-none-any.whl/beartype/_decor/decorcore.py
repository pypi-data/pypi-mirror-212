#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2023 Beartype authors.
# See "LICENSE" for further details.

'''
**Unmemoized beartype decorator.**

This private submodule defines all core high-level logic underlying the
:func:`beartype.beartype` decorator, whose implementation in the parent
:mod:`beartype._decor._cache.cachedecor` submodule is a thin wrapper
efficiently memoizing closures internally created and returned by that
decorator. In turn, those closures directly defer to this submodule.

This private submodule is effectively the :func:`beartype.beartype` decorator
despite *not* actually being that decorator (due to being unmemoized).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar import (
    BeartypeException,
    BeartypeDecorWrappeeException,
    BeartypeDecorWrapperException,
    # BeartypeWarning,
)
from beartype.typing import no_type_check
from beartype._cave._cavefast import (
    MethodBoundInstanceOrClassType,
    MethodDecoratorBuiltinTypes,
    MethodDecoratorClassType,
    MethodDecoratorPropertyType,
    MethodDecoratorStaticType,
)
from beartype._cave._cavemap import NoneTypeOr
from beartype._conf.confcls import BeartypeConf
from beartype._conf.confenum import BeartypeStrategy
from beartype._data.datatyping import (
    BeartypeableT,
    TypeStack,
    TypeWarning,
)
from beartype._data.cls.datacls import TYPES_BEARTYPEABLE
from beartype._decor._wrap.wrapmain import generate_code
from beartype._check.checkcall import BeartypeCall
from beartype._util.cache.pool.utilcachepoolobjecttyped import (
    acquire_object_typed,
    release_object_typed,
)
from beartype._util.func.lib.utilbeartypefunc import (
    is_func_unbeartypeable,
    set_func_beartyped,
)
from beartype._util.func.utilfuncmake import make_func
from beartype._util.func.utilfunctest import is_func_python
from beartype._util.text.utiltextansi import strip_text_ansi
from beartype._util.text.utiltextlabel import label_object_context
from beartype._util.text.utiltextmunge import uppercase_char_first
from beartype._util.text.utiltextprefix import prefix_beartypeable
from traceback import format_exc
from warnings import warn

# ....................{ DECORATORS                         }....................
def beartype_object(
    # Mandatory parameters.
    obj: BeartypeableT,
    conf: BeartypeConf,

    # Optional parameters.
    cls_stack: TypeStack = None,
) -> BeartypeableT:
    '''
    Decorate the passed **beartypeable** (i.e., caller-defined object that may
    be decorated by the :func:`beartype.beartype` decorator) with optimal
    type-checking dynamically generated unique to that beartypeable.

    Parameters
    ----------
    obj : BeartypeableT
        **Beartypeable** (i.e., pure-Python callable or class) to be decorated.
    conf : BeartypeConf
        **Beartype configuration** (i.e., dataclass encapsulating all flags,
        options, settings, and other metadata configuring the current decoration
        of the decorated callable or class).
    cls_stack : TypeStack, optional
        **Type stack** (i.e., either a tuple of the one or more
        :func:`beartype.beartype`-decorated classes lexically containing the
        class variable or method annotated by this hint *or* :data:`None`).
        Defaults to :data:`None`.

    Returns
    ----------
    BeartypeableT
        Either:

        * If the passed object is a class, this existing class embellished with
          dynamically generated type-checking.
        * If the passed object is a callable, a new callable wrapping that
          callable with dynamically generated type-checking.

    See Also
    ----------
    :func:`beartype._decor.decormain.beartype`
        Memoized parent decorator wrapping this unmemoized child decorator.
    '''
    # print(f'Decorating object {repr(obj)}...')

    # If this object is a class, return this class decorated with type-checking.
    #
    # Note that the passed "cls_curr" class is ignorable in this context.
    # Why? There are three cases. "obj" is either a:
    # * Root decorated class, in which case both "cls_root" and
    #   "cls_curr" are "None". Ergo, "cls_curr" conveys *NO*
    #   meaningful semantics.
    # * Inner decorated class of a root decorated class, in which case both
    #   "cls_root" and "cls_curr" refer to that root decorated case.
    #   Ergo, "cls_curr" conveys *NO* additional meaningful semantics.
    # * Leaf decorated class of an inner decorated class of a root decorated
    #   class, in which case "cls_root" and "cls_curr" refer to
    #   different classes. However, lexical scoping rules in Python prevent
    #   leaf classes from directly referring to any parent classes *OTHER* than
    #   module-scoped root classes. Ergo, "cls_curr" conveys *NO*
    #   meaningful semantics again.
    #
    # In all cases, "cls_curr" conveys *NO* meaningful semantics.
    if isinstance(obj, type):
        # print(f'Decorating type {repr(obj)}...')
        return _beartype_type(  # type: ignore[return-value]
            cls=obj,
            conf=conf,
            cls_stack=cls_stack,
        )
    # Else, this object is a non-class.
    # print(f'Decorating non-type {repr(obj)}...')

    # Type of this object.
    obj_type = type(obj)

    # If this object is an uncallable builtin method descriptor (i.e., either a
    # property, class method, instance method, or static method object),
    # @beartype was listed above rather than below the builtin decorator
    # generating this descriptor in the chain of decorators decorating this
    # decorated callable. Although @beartype typically *MUST* decorate a
    # callable directly, this edge case is sufficiently common *AND* trivial to
    # resolve to warrant doing so. To do so, this conditional branch effectively
    # reorders @beartype to be the first decorator decorating the pure-Python
    # function underlying this method descriptor: e.g.,
    #
    #     # This branch detects and reorders this edge case...
    #     class MuhClass(object):
    #         @beartype
    #         @classmethod
    #         def muh_classmethod(cls) -> None: pass
    #
    #     # ...to resemble this direct decoration instead.
    #     class MuhClass(object):
    #         @classmethod
    #         @beartype
    #         def muh_classmethod(cls) -> None: pass
    #
    # Note that most but *NOT* all of these objects are uncallable. Regardless,
    # *ALL* of these objects are unsuitable for direct decoration. Specifically:
    # * Under Python < 3.10, *ALL* of these objects are uncallable.
    # * Under Python >= 3.10:
    #   * Descriptors created by @classmethod and @property are uncallable.
    #   * Descriptors created by @staticmethod are technically callable but
    #     C-based and thus unsuitable for decoration.
    if obj_type in MethodDecoratorBuiltinTypes:
        return _beartype_decorator_builtin(  # type: ignore[return-value]
            descriptor=obj,
            conf=conf,
            cls_stack=cls_stack,
        )
    # Else, this object is *NOT* an uncallable builtin method descriptor.
    #
    # If this object is uncallable, raise an exception.
    elif not callable(obj):
        # Raise an exception.
        raise BeartypeDecorWrappeeException(
            f'Uncallable {repr(obj)} not decoratable by @beartype.')
    # Else, this object is callable.
    #
    # If this object is *NOT* a pure-Python function, attempt to monkey-patch
    # runtime type-checking into this object by replacing all bound method
    # descriptors of this object with comparable descriptors calling
    # @beartype-generated runtime type-checking wrapper functions.
    elif not is_func_python(obj):
        return _monkeypatch_object(  # type: ignore[return-value]
            obj=obj,
            conf=conf,
            cls_stack=cls_stack,
        )
    # Else, this object is a pure-Python function.

    # Return a new callable decorating that callable with type-checking.
    return _beartype_func(  # type: ignore[return-value]
        func=obj,
        conf=conf,
        cls_stack=cls_stack,
    )


#FIXME: Unit test us up, please.
def beartype_object_nonfatal(
    # Mandatory parameters.
    obj: BeartypeableT,
    warning_category: TypeWarning,

    # Optional parameters.
    **kwargs
) -> BeartypeableT:
    '''
    Decorate the passed **beartypeable** (i.e., pure-Python callable or class)
    with optimal type-checking dynamically generated unique to that
    beartypeable and any otherwise uncaught exception raised by doing so safely
    coerced into a warning instead.

    Motivation
    ----------
    This decorator is principally intended to be called by our **all-at-once
    API** (i.e., the import hooks defined by the :mod:`beartype.claw`
    subpackage). Raising detailed exception tracebacks on unexpected error
    conditions is:

    * The right thing to do for callables and classes manually type-checked with
      the :func:`beartype.beartype` decorator.
    * The wrong thing to do for callables and classes automatically type-checked
      by import hooks installed by public functions exported by the
      :mod:`beartype.claw` subpackage. Why? Because doing so would render those
      import hooks fragile to the point of being practically useless on
      real-world packages and codebases by unexpectedly failing on the first
      callable or class defined *anywhere* under a package that is not
      type-checkable by :func:`beartype.beartype` (whether through our fault or
      that package's). Instead, the right thing to do is to:

      * Emit a warning for each callable or class that :func:`beartype.beartype`
        fails to generate a type-checking wrapper for.
      * Continue to the next callable or class.

    Parameters
    ----------
    obj : BeartypeableT
        **Beartypeable** (i.e., pure-Python callable or class) to be decorated.
    warning_category : TypeWarning
        Category of the non-fatal warning to emit if :func:`beartype.beartype`
        fails to generate a type-checking wrapper for this callable or class.

    All remaining keyword parameters are passed as is to the lower-level
    :func:`.beartype_object` decorator internally called by this higher-level
    decorator on the passed beartypeable.

    Returns
    ----------
    BeartypeableT
        Either:

        * If :func:`.beartype_object` raises an exception, the passed object
          unmodified as is.
        * If :func:`.beartype_object` raises no exception:
          * If the passed object is a class, this existing class embellished with
            dynamically generated type-checking.
          * If the passed object is a callable, a new callable wrapping that
            callable with dynamically generated type-checking.

    Warns
    ----------
    warning_category
        If :func:`.beartype_object` fails to generate a type-checking wrapper
        for this callable or class by raising a fatal exception, this function
        coerces that exception into a non-fatal warning describing that error.
    '''

    # Attempt to decorate the passed beartypeable.
    try:
        return beartype_object(obj, **kwargs)
    # If doing so unexpectedly raises an exception, coerce that fatal exception
    # into a non-fatal warning for nebulous safety.
    except Exception as exception:
        assert isinstance(warning_category, Warning), (
            f'{repr(warning_category)} not warning category.')

        # Original error message to be embedded in the warning message to be
        # emitted, stripped of *ALL* ANSI color. While colors improve the
        # readability of exception messages that percolate down to an ANSI-aware
        # command line, warnings are usually harvested and then regurgitated by
        # intermediary packages into ANSI-unaware logfiles.
        #
        # This message is defined as either...
        error_message = strip_text_ansi(
            # If this exception is beartype-specific, this exception's message
            # is probably human-readable as is. In this case, coerce only that
            # message directly into a warning for brevity and readability.
            str(exception)
            if isinstance(exception, BeartypeException) else
            # Else, this exception is *NOT* beartype-specific. In this case,
            # this exception's message is probably *NOT* human-readable as is.
            # Prepend that non-human-readable message by this exception's
            # traceback for disambiguity and debuggability. Note that the
            # format_exc() function appends this exception's message to this
            # traceback and thus suffices as is.
            format_exc()
        )

        # Indent this exception message by globally replacing *EVERY* newline in
        # this message with a newline followed by four spaces. Doing so visually
        # offsets this lower-level exception message from the higher-level
        # warning message embedding this exception message below.
        error_message = error_message.replace('\n', '\n    ')

        # Warning message to be emitted, consisting of:
        # * A human-readable label contextually describing this beartypeable,
        #   capitalized such that the first character is uppercase.
        # * This indented exception message.
        warning_message = uppercase_char_first(
            f'{prefix_beartypeable(obj)}{label_object_context(obj)}:\n'
            f'{error_message}'
        )

        # Emit this message under this category.
        warn(warning_message, warning_category)

    # Return this object unmodified, as @beartype failed to successfully wrap
    # this object with a type-checking class or callable. So it goes, fam.
    return obj  # type: ignore[return-value]

# ....................{ PRIVATE ~ beartypers : func        }....................
def _beartype_decorator_builtin(
    # Mandatory parameters.
    descriptor: BeartypeableT,
    conf: BeartypeConf,

    # Variadic keyword parameters.
    **kwargs
) -> BeartypeableT:
    '''
    Decorate the passed **builtin decorator object** (i.e., C-based unbound
    method descriptor produced by the builtin :class:`classmethod`,
    :class:`property`, or :class:`staticmethod` decorators) with dynamically
    generated type-checking.

    Parameters
    ----------
    descriptor : BeartypeableT
        Descriptor to be decorated by :func:`beartype.beartype`.
    conf : BeartypeConf
        Beartype configuration configuring :func:`beartype.beartype` uniquely
        specific to this descriptor.

    All remaining keyword parameters are passed as is to the lower-level
    :func:`_beartype_func` decorator internally called by this higher-level
    decorator on the pure-Python function encapsulated in this descriptor.

    Returns
    ----------
    BeartypeableT
        New pure-Python callable wrapping this descriptor with type-checking.

    Raises
    ----------
    BeartypeDecorWrappeeException
        If this descriptor is neither a class, property, or static method
        descriptor.
    '''
    # assert isinstance(descriptor, MethodDecoratorBuiltinTypes), (
    #     f'{repr(descriptor)} not builtin method descriptor.')
    # assert isinstance(conf, BeartypeConf), f'{repr(conf)} not configuration.'

    # Type of this descriptor.
    descriptor_type = type(descriptor)

    # If this descriptor is a property method...
    #
    # Note that property method descriptors are intentionally tested next, due
    # to their ubiquity "in the wild." Class and static method descriptors are
    # comparatively rarefied by comparison.
    if descriptor_type is MethodDecoratorPropertyType:
        # Pure-Python unbound getter, setter, and deleter functions wrapped by
        # this descriptor if any *OR* "None" otherwise (i.e., for each such
        # function currently unwrapped by this descriptor).
        descriptor_getter  = descriptor.fget  # type: ignore[assignment,union-attr]
        descriptor_setter  = descriptor.fset  # type: ignore[assignment,union-attr]
        descriptor_deleter = descriptor.fdel  # type: ignore[assignment,union-attr]

        # Decorate this getter function with type-checking.
        #
        # Note that *ALL* property method descriptors wrap at least a getter
        # function (but *NOT* necessarily a setter or deleter function). This
        # function is thus guaranteed to be non-"None".
        descriptor_getter = _beartype_func(  # type: ignore[type-var]
            func=descriptor_getter,  # pyright: ignore[reportGeneralTypeIssues]
            conf=conf,
            **kwargs
        )

        # If this property method descriptor additionally wraps a setter and/or
        # deleter function, type-check those functions as well.
        if descriptor_setter is not None:
            descriptor_setter = _beartype_func(
                func=descriptor_setter,
                conf=conf,
                **kwargs
            )
        if descriptor_deleter is not None:
            descriptor_deleter = _beartype_func(
                func=descriptor_deleter,
                conf=conf,
                **kwargs
            )

        # Return a new property method descriptor decorating all of these
        # functions, implicitly destroying the prior descriptor.
        #
        # Note that the "property" class interestingly has this signature:
        #     class property(fget=None, fset=None, fdel=None, doc=None): ...
        return property(  # type: ignore[return-value]
            fget=descriptor_getter,
            fset=descriptor_setter,
            fdel=descriptor_deleter,
            doc=descriptor.__doc__,
        )
    # Else, this descriptor is *NOT* a property method.
    #
    # If this descriptor is a class method...
    elif descriptor_type is MethodDecoratorClassType:
        # Pure-Python unbound function type-checking this class method.
        func_checked = _beartype_func(
            func=descriptor.__func__,  # type: ignore[union-attr]
            conf=conf,
            **kwargs
        )

        # Return a new class method descriptor decorating the pure-Python
        # unbound function wrapped by this descriptor with type-checking,
        # implicitly destroying the prior descriptor.
        return classmethod(func_checked)  # type: ignore[return-value]
    # Else, this descriptor is *NOT* a class method.
    #
    # If this descriptor is a static method...
    elif descriptor_type is MethodDecoratorStaticType:
        # Pure-Python unbound function type-checking this static method.
        func_checked = _beartype_func(
            func=descriptor.__func__,  # type: ignore[union-attr]
            conf=conf,
            **kwargs
        )

        # Return a new static method descriptor decorating the pure-Python
        # unbound function wrapped by this descriptor with type-checking,
        # implicitly destroying the prior descriptor.
        return staticmethod(func_checked)  # type: ignore[return-value]
    # Else, this descriptor is *NOT* a static method.

    # Raise a fallback exception. This should *NEVER happen. This *WILL* happen.
    raise BeartypeDecorWrappeeException(
        f'Builtin method descriptor {repr(descriptor)} '
        f'not decoratable by @beartype '
        f'(i.e., neither property, class method, nor static method descriptor).'
    )


def _beartype_method_bound(
    # Mandatory parameters.
    descriptor: BeartypeableT,
    conf: BeartypeConf,

    # Variadic keyword parameters.
    **kwargs
) -> BeartypeableT:
    '''
    Decorate the passed **builtin bound method object** (i.e., C-based bound
    method descriptor produced by Python on instantiation for each instance and
    class method defined by the class being instantiated) with dynamically
    generated type-checking.

    Parameters
    ----------
    descriptor : BeartypeableT
        Descriptor to be decorated by :func:`beartype.beartype`.
    conf : BeartypeConf
        Beartype configuration configuring :func:`beartype.beartype` uniquely
        specific to this descriptor.

    All remaining keyword parameters are passed as is to the lower-level
    :func:`_beartype_func` decorator internally called by this higher-level
    decorator on the pure-Python function encapsulated in this descriptor.

    Returns
    ----------
    BeartypeableT
        New pure-Python callable wrapping this descriptor with type-checking.
    '''
    assert isinstance(descriptor, MethodBoundInstanceOrClassType), (
        f'{repr(descriptor)} not builtin bound method descriptor.')

    # Pure-Python unbound function encapsulated by this descriptor.
    descriptor_func_old = descriptor.__func__

    # Pure-Python unbound function decorating the similarly pure-Python unbound
    # function encapsulated by this descriptor with type-checking.
    #
    # Note that doing so:
    # * Implicitly propagates dunder attributes (e.g., "__annotations__",
    #   "__doc__") from the original function onto this new function. Good.
    # * Does *NOT* implicitly propagate the same dunder attributes from the
    #   original descriptor encapsulating the original function to the new
    #   descriptor (created below) encapsulating this wrapper function. Bad!
    #   Thankfully, only one such attribute exists as of this time: "__doc__".
    #   We propagate this attribute manually below.
    descriptor_func_new = _beartype_func(func=descriptor_func_old, conf=conf)  # pyright: ignore[reportGeneralTypeIssues]

    # New instance method descriptor rebinding this function to the instance of
    # the class bound to the prior descriptor.
    #
    # Note that:
    # * This is required, as the "__func__" attribute of method descriptors is
    #   read-only. Attempting to do so raises this non-human-readable exception:
    #     AttributeError: readonly attribute
    #   This implies that the passed descriptor *CANNOT* be meaningfully
    #   modified. Our only recourse is to define an entirely new descriptor,
    #   effectively discarding the passed descriptor, which will then be
    #   subsequently garbage-collected. This is wasteful. This is Python.
    # * This can also be implemented by abusing the descriptor protocol:
    #       descriptor_new = descriptor_func_new.__get__(descriptor.__self__)
    #   That said, there exist *NO* benefits to doing so. Indeed, doing so only
    #   reduces the legibility and maintainability of this operation.
    descriptor_new = MethodBoundInstanceOrClassType(
        descriptor_func_new, descriptor.__self__)  # type: ignore[return-value]

    #FIXME: Actually, Python doesn't appear to support this at the moment.
    #Attempting to do so raises this exception:
    #    AttributeError: attribute '__doc__' of 'method' objects is not writable
    #
    #See also this open issue on the Python bug tracker requesting this be
    #resolved. Sadly, Python has yet to resolve this:
    #    https://bugs.python.org/issue47153
    # # Propagate the docstring from the prior to the new descriptor.
    # #
    # # Note that Python guarantees this attribute to exist. If the original
    # # function had a docstring, this attribute is non-"None"; else, this
    # # attribute is "None". In either case, this attribute exists. Ergo,
    # # additional validation is neither required nor desired.
    # descriptor_new.__doc__ = descriptor.__doc__

    # Return this new descriptor, implicitly destroying the prior descriptor.
    return descriptor_new  # type: ignore[return-value]


def _beartype_func(
    # Mandatory parameters.
    func: BeartypeableT,
    conf: BeartypeConf,

    # Variadic keyword parameters.
    **kwargs
) -> BeartypeableT:
    '''
    Decorate the passed callable with dynamically generated type-checking.

    Parameters
    ----------
    func : BeartypeableT
        Callable to be decorated by :func:`beartype.beartype`.
    conf : BeartypeConf
        Beartype configuration configuring :func:`beartype.beartype` uniquely
        specific to this callable.

    All remaining keyword parameters are passed as is to the
    :meth:`BeartypeCall.reinit` method.

    Returns
    ----------
    BeartypeableT
        New pure-Python callable wrapping this callable with type-checking.
    '''
    assert callable(func), f'{repr(func)} uncallable.'
    # assert isinstance(conf, BeartypeConf), f'{repr(conf)} not configuration.'
    # assert isinstance(cls_root, NoneTypeOr[type]), (
    #     f'{repr(cls_root)} neither type nor "None".')
    # assert isinstance(cls_curr, NoneTypeOr[type]), (
    #     f'{repr(cls_curr)} neither type nor "None".')

    #FIXME: Uncomment to display all annotations in "pytest" tracebacks.
    # func_hints = func.__annotations__

    # If this configuration enables the no-time strategy performing *NO*
    # type-checking, monkey-patch that callable with the standard
    # @typing.no_type_check decorator detected above by the call to the
    # is_func_unbeartypeable() tester on all subsequent decorations passed the
    # same callable. (Doing so prevents all subsequent decorations from
    # erroneously ignoring this previously applied no-time strategy.)
    if conf.strategy is BeartypeStrategy.O0:
        no_type_check(func)
    # Else, this configuration enables a positive-time strategy performing at
    # least the minimal amount of type-checking.

    # If that callable is unbeartypeable (i.e., if this decorator should
    # preserve that callable as is rather than wrap that callable with
    # constant-time type-checking), silently reduce to the identity decorator.
    #
    # Note that this conditional implicitly handles the prior conditional! :O
    if is_func_unbeartypeable(func):  # type: ignore[arg-type]
        return func  # type: ignore[return-value]
    # Else, that callable is beartypeable. Let's do this, folks.

    # Previously cached callable metadata reinitialized from that callable.
    bear_call = acquire_object_typed(BeartypeCall)
    bear_call.reinit(func, conf, **kwargs)

    # Generate the raw string of Python statements implementing this wrapper.
    func_wrapper_code = generate_code(bear_call)

    # If that callable requires *NO* type-checking, silently reduce to a noop
    # and thus the identity decorator by returning that callable as is.
    if not func_wrapper_code:
        return func  # type: ignore[return-value]
    # Else, that callable requires type-checking. Let's *REALLY* do this, fam.

    # Function wrapping that callable with type-checking to be returned.
    #
    # For efficiency, this wrapper accesses *ONLY* local rather than global
    # attributes. The latter incur a minor performance penalty, since local
    # attributes take precedence over global attributes, implying all global
    # attributes are *ALWAYS* first looked up as local attributes before falling
    # back to being looked up as global attributes.
    func_wrapper = make_func(
        func_name=bear_call.func_wrapper_name,
        func_code=func_wrapper_code,
        func_locals=bear_call.func_wrapper_scope,

        #FIXME: String formatting is infamously slow. As an optimization, it'd
        #be strongly preferable to instead pass a lambda function accepting *NO*
        #parameters and returning the desired string, which make_func() should
        #then internally call on an as-needed basis to make this string: e.g.,
        #    func_label_factory=lambda: f'@beartyped {bear_call.func_wrapper_name}() wrapper',
        #
        #This is trivial. The only question then is: "Which is actually faster?"
        #Before finalizing this refactoring, let's profile both, adopt whichever
        #outperforms the other, and then document this choice in make_func().
        func_label=f'@beartyped {bear_call.func_wrapper_name}() wrapper',

        func_wrapped=func,
        is_debug=conf.is_debug,
        exception_cls=BeartypeDecorWrapperException,
    )

    # Declare this wrapper to be generated by @beartype, which tests for the
    # existence of this attribute above to avoid re-decorating callables
    # already decorated by @beartype by efficiently reducing to a noop.
    set_func_beartyped(func_wrapper)

    # Release this callable metadata back to its object pool.
    release_object_typed(bear_call)

    # Return this wrapper.
    return func_wrapper  # type: ignore[return-value]

# ....................{ PRIVATE ~ beartypers : type        }....................
def _beartype_type(
    # Mandatory parameters.
    cls: BeartypeableT,
    conf: BeartypeConf,

    # Optional parameters.
    cls_stack: TypeStack = None,
) -> BeartypeableT:
    '''
    Decorate the passed class with dynamically generated type-checking.

    Parameters
    ----------
    cls : BeartypeableT
        Class to be decorated by :func:`beartype.beartype`.
    conf : BeartypeConf
        Beartype configuration configuring :func:`beartype.beartype` uniquely
        specific to this class.
    cls_stack : TypeStack, optional
        **Type stack** (i.e., either a tuple of the one or more
        :func:`beartype.beartype`-decorated classes lexically containing the
        class variable or method annotated by this hint *or* :data:`None`).
        Defaults to :data:`None`.

    Returns
    ----------
    BeartypeableT
        This class decorated by :func:`beartype.beartype`.
    '''
    assert isinstance(cls, type), f'{repr(cls)} not type.'
    assert isinstance(cls_stack, NoneTypeOr[tuple]), (
        f'{repr(cls_stack)} neither tuple nor "None".')
    # assert isinstance(conf, BeartypeConf), f'{repr(conf)} not configuration.'

    #FIXME: Insufficient. We also want to set a beartype-specific dunder
    #attribute -- say, "__beartyped" -- on this class. Additionally, if this
    #class has already been @beartyped, we want to detect that here and avoid
    #re-@beartype-ing this class. In short, we want to generalize our existing
    #"beartype._util.func.lib.utilbeartypefunc" submodule to support classes as
    #well. Let's shift that submodule somewhere more general, please. Perhaps:
    #* Rename "beartype._util.func.lib.utilbeartypefunc" to
    #  "beartype._util.check.utilcheckfunc".
    #* Define a new "beartype._util.check.utilchecktype" submodule containing
    #  similar class-specific functionality.
    #FIXME: Unit test us up, please. Test against at least:
    #* A dataclass. We already do this, of course. Hurrah!
    #* An uncallable class (i.e., defining *NO* __call__() dunder method)
    #  defining at least:
    #  * A class variable (e.g., "muh_classvar: ClassVar[int] = 42").
    #  * A standard instance method.
    #  * A class method.
    #  * A static method.
    #  * A property getter, setter, and deleter.
    #* A callable class (i.e., defining a __call__() dunder method).
    #* A PEP 563-fueled self-referential class. See this as a simple example:
    #     https://github.com/beartype/beartype/issues/152#issuecomment-1197778501

    # Replace the passed class stack with a new class stack appending this
    # decorated class to the top of this stack, reflecting the fact that this
    # decorated class is now the most deeply lexically nested class for the
    # currently recursive chain of @beartype-decorated classes.
    cls_stack = (
        # If the caller passed *NO* class stack, then this class is necessarily
        # the first decorated class being decorated directly by @beartype and
        # thus the root decorated class.
        #
        # Note this is the common case and thus tested first. Since nested
        # classes effectively do *NOT* exist in the wild, this comprises
        # 99.999% of all real-world cases.
        (cls,)
        if cls_stack is None else
        # Else, the caller passed a clack stack comprising at least a root
        # decorated class. Preserve that class as is to properly expose that
        # class elsewhere.
        cls_stack + (cls,)
    )

    # For the unqualified name and value of each direct (i.e., *NOT* indirectly
    # inherited) attribute of this class...
    for attr_name, attr_value in cls.__dict__.items():  # pyright: ignore[reportGeneralTypeIssues]
        # If this attribute is beartypeable...
        if isinstance(attr_value, TYPES_BEARTYPEABLE):
            # This attribute decorated with type-checking configured by this
            # configuration if *NOT* already decorated.
            attr_value_beartyped = beartype_object(
                obj=attr_value,
                conf=conf,
                cls_stack=cls_stack,
            )

            # Replace this undecorated attribute with this decorated attribute.
            #
            # Note that class attributes are *ONLY* settable by calling the
            # tragically slow setattr() builtin. Attempting to directly set an
            # attribute on the class dictionary raises an exception. Why? Because
            # class dictionaries are actually low-level "mappingproxy" objects that
            # intentionally override the __setattr__() dunder method to
            # unconditionally raise an exception. Why? Because this constraint
            # enables the type.__setattr__() dunder method to enforce critical
            # efficiency constraints on class attributes -- including that class
            # attribute keys are not only strings but valid Python identifiers:
            #     >>> class OhGodHelpUs(object): pass
            #     >>> OhGodHelpUs.__dict__['even_god_cannot_help'] = 2
            #     TypeError: 'mappingproxy' object does not support item assignment
            #
            # See also this relevant StackOverflow answer by Python luminary
            # Raymond Hettinger:
            #     https://stackoverflow.com/a/32720603/2809027
            setattr(cls, attr_name, attr_value_beartyped)
        # Else, this attribute is *NOT* beartypeable. In this case, silently
        # ignore this attribute.

    # Return this class as is.
    return cls  # type: ignore[return-value]

# ....................{ PRIVATE ~ patchers                 }....................
#FIXME: Generalize to iteratively monkey-patch *ALL* bound method descriptors of
#this object. Currently, this method only monkey-patches the __call__() method.
#Note that doing so will prove slightly non-trivial, as we'll need to handle
#both:
#* Special dunder methods like __call__() and __getitem__(), which Python
#  ignores unless defined on the *CLASS* of this object rather than this object
#  itself.
#* All other methods, which should be defined on this object itself for safety.
def _monkeypatch_object(
    # Mandatory parameters.
    obj: BeartypeableT,
    conf: BeartypeConf,

    # Variadic keyword parameters.
    **kwargs
) -> BeartypeableT:
    '''
    Monkey-patch the passed **arbitrary object** (i.e., pure-Python object
    assumed *not* to be handled by other higher-level decorators defined by this
    submodule and thus neither a class, function, nor builtin decorator
    descriptor) with dynamically generated type-checking.

    For each bound method descriptor encapsulating a method bound to this
    object, this function monkey-patches (i.e., replaces) that descriptor with a
    comparable descriptor calling a new :func:`beartype.beartype`-generated
    runtime type-checking wrapper function wrapping the original method.

    Parameters
    ----------
    obj : BeartypeableT
        Object to be monkey-patched by :func:`beartype.beartype`.
    conf : BeartypeConf
        Beartype configuration configuring :func:`beartype.beartype` uniquely
        specific to this descriptor.

    All remaining keyword parameters are passed as is to the lower-level
    :func:`._beartype_func` decorator internally called by this higher-level
    decorator on the pure-Python function encapsulated in this descriptor.

    Returns
    ----------
    BeartypeableT
        The object monkey-patched by :func:`beartype.beartype`.
    '''
    # print(f'@beartyping pseudo-callable {repr(obj)}...')

    # __call__() dunder method defined by this object if this object defines
    # this method *OR* "None" otherwise.
    obj_call_method = getattr(obj, '__call__')

    # If this object does *NOT* define this method, this object is *NOT* a
    # pseudo-callable. In this case, raise an exception.
    #
    # Note this edge case should *NEVER* occur. By definition, this object has
    # already been validated to be callable. But this object is *NOT* a
    # pure-Python function. Since the only other category of callable in Python
    # is a pseudo-callable, this object *MUST* be a pseudo-callable. That said,
    # languages change; it's not inconceivable that Python could introduce yet
    # another kind of callable object under future versions.
    if obj_call_method is None:
        raise BeartypeDecorWrappeeException(  # pragma: no cover
            f'Callable {repr(obj)} not pseudo-callable (i.e., callable '
            f'object defining __call__() dunder method).'
        )
    # Else, this object is a pseudo-callable.

    # Replace the existing bound method descriptor to this __call__() dunder
    # method  with a new bound method descriptor to a new __call__() dunder
    # method wrapping the old method with runtime type-checking.
    #
    # Note that:
    # * This is a monkey-patch. Since the caller is intentionally decorating
    #   this pseudo-callable with @beartype, this is exactly what the caller
    #   wanted. Probably.
    # * This monkey-patches the *CLASS* of this object rather than this object
    #   itself. Why? Because Python. For unknown reasons (so, speed is what
    #   we're saying), Python accesses dunder methods on the *CLASS* of an
    #   object rather than on the object itself. Of course, this implies that
    #   *ALL* instances of this pseudo-callable (rather than
    #   merely the passed instance) will be monkey-patched. This may *NOT*
    #   necessarily be what the caller wanted. Unfortunately, the only
    #   alternative would be for @beartype to raise an exception when passed a
    #   pseudo-callable. Since doing something beneficial is generally
    #   preferable to doing something harmful, @beartype prefers the former. See
    #   also official documentation on the subject:
    #       https://docs.python.org/3/reference/datamodel.html#special-method-names
    obj.__class__.__call__ = _beartype_method_bound(  # type: ignore[assignment,method-assign]
        descriptor=obj_call_method,
        conf=conf,
        **kwargs,
    )

    # Return this monkey-patched object.
    return obj  # type: ignore[return-value]
