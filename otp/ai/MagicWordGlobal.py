from direct.showbase import PythonUtil

MINIMUM_MAGICWORD_ACCESS = 200 # vip

class MagicError(Exception): pass

def ensureAccess(access, msg='Insufficient access'):
    if spellbook.getInvokerAccess() < access:
        raise MagicError(msg)

class Spellbook:
    """
    The Spellbook manages the list of all Magic Words that have been registered
    anywhere in the system. When the MagicWordManager(AI) wants to process a
    Magic Word, it is passed off to the Spellbook, which performs the operation.

    To add Magic Words to the Spellbook, use the @magicWord() decorator.
    """

    def __init__(self):
        self.words = {}

        self.currentInvoker = None
        self.currentTarget = None

    def addWord(self, word):
        self.words[word.name] = word

    def process(self, invoker, target, incantation):
        self.currentInvoker = invoker
        self.currentTarget = target
        word, args = (incantation.split(' ', 1) + [''])[:2]

        try:
            return self.doWord(word, args)
        except MagicError as e:
            return e.message
        except Exception:
            return PythonUtil.describeException(backTrace=1)
        finally:
            self.currentInvoker = None
            self.currentTarget = None

    def doWord(self, wordName, args):
        word = self.words.get(wordName)
        if not word:
            return

        ensureAccess(word.access)
        if self.getTarget() and self.getTarget() != self.getInvoker():
            if self.getInvokerAccess() <= self.getTarget().getAdminAccess():
                raise MagicError('Target must have lower access')

        result = word.run(args)
        if result is not None:
            return str(result)

    def getInvoker(self):
        return self.currentInvoker

    def getTarget(self):
        return self.currentTarget

    def getInvokerAccess(self):
        if not self.currentInvoker:
            return 0
        return self.currentInvoker.getAdminAccess()
        
    def __repr__(self):
        r = ''
        accessToJob = {200: 'VIP', 300: 'MOD', 400: 'DEV', 500: 'ADMIN', 1000: 'TOP ADMIN'}
        for name, word in self.words.items():
            access = word.access
            job = accessToJob.get(access)
            if job is None:
                if access > 500:
                    job = accessToJob[1000]
                    
                else:
                    job = 'UNKNOWN JOB'
                    
            r += '%s: %d (%s)\n' % (name, access, job)
            
        return r

spellbook = Spellbook()

# CATEGORIES
class MagicWordCategory:
    def __init__(self, name, defaultAccess=500):
        self.name = name
        self.defaultAccess = defaultAccess

CATEGORY_UNKNOWN = MagicWordCategory('Unknown')
CATEGORY_GRAPHICAL = MagicWordCategory('Graphical debugging', defaultAccess=400)
CATEGORY_GUI = MagicWordCategory('GUI debugging', defaultAccess=400)
CATEGORY_MOBILITY = MagicWordCategory('Mobility cheats', defaultAccess=300)
CATEGORY_HEAD = MagicWordCategory('God commands', defaultAccess=1000)
CATEGORY_ADM = MagicWordCategory('Administrator commands', defaultAccess=500)
CATEGORY_CHEAT = MagicWordCategory('Game cheats', defaultAccess=400)
CATEGORY_CHARACTERSTATS = MagicWordCategory('Character-stats cheats', defaultAccess=300)
CATEGORY_CHARACTERSTATS2 = MagicWordCategory('Character-stats cheats', defaultAccess=400)
CATEGORY_DEBUG = MagicWordCategory('Debug cheats', defaultAccess=400)
CATEGORY_MODERATION = MagicWordCategory('Moderation commands', defaultAccess=300)
CATEGORY_FUN = MagicWordCategory('Fun commands', defaultAccess=200)


class MagicWord:
    def __init__(self, name, func, types, access, doc):
        self.name = name
        self.func = func
        self.types = types
        self.access = access
        self.doc = doc

    def parseArgs(self, string):
        maxArgs = self.func.func_code.co_argcount
        minArgs = maxArgs - (len(self.func.func_defaults) if self.func.func_defaults else 0)

        args = string.split(None, maxArgs-1)[:maxArgs]
        if len(args) < minArgs:
            raise MagicError('Magic word %s requires at least %d arguments' % (self.name, minArgs))

        output = []
        for i, (type, arg) in enumerate(zip(self.types, args)):
            try:
                targ = type(arg)
            except (TypeError, ValueError):
                raise MagicError('Argument %d of magic word %s must be %s' % (i, self.name, type.__name__))

            output.append(targ)

        return output

    def run(self, rawArgs):
        args = self.parseArgs(rawArgs)
        return self.func(*args)


class MagicWordDecorator:
    """
    This class manages Magic Word decoration. It is aliased as magicWord, so that
    the @magicWord(...) construct instantiates this class and has the resulting
    object process the Magic Word's construction.
    """

    def __init__(self, name=None, types=[str], access=None, category=CATEGORY_UNKNOWN):
        self.name = name
        self.types = types
        self.category = category
        if access is not None:
            self.access = access
        else:
            self.access = self.category.defaultAccess

    def __call__(self, mw):
        # This is the actual decoration routine. We add the function 'mw' as a
        # Magic Word to the Spellbook, using the attributes specified at construction
        # time.

        name = self.name
        if name is None:
            name = mw.func_name

        word = MagicWord(name, mw, self.types, self.access, mw.__doc__)
        spellbook.addWord(word)

        return mw

magicWord = MagicWordDecorator
