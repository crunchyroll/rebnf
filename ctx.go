// chris 072915

package rebnf

// Ctx is a context for making Random calls.  It provides several limits
// to the recursive grammar-walking algorithm to help limit its output.
type Ctx struct {
	maxreps  int
	maxdepth int
}

// NewCtx creates a new Ctx, ready to make Random calls.  Pass in two
// limits.  The first is the maximum repetitions--the largest number of
// times that an EBNF repetition will be repeated.  In its production,
// when Random encounters a repetition, it will choose a random number
// of times to repeat it in [0, maxRepetitions].  The second is the
// recursion depth limit.  It does not truly limit the depth of the
// recursion, but when this limit is surpassed, the algorithm will favor
// pursuing terminal symbols over non-terminal ones in order to wrap up
// production quickly while still ensuring that the production is an
// instance of the language specified by the grammar.
func NewCtx(maxRepetitions, maxRecursionDepth int) *Ctx {
	return &Ctx{maxreps: maxRecursionDepth, maxdepth: maxRecursionDepth}
}