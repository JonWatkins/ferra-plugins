[
  (do_block) (else_block) (rescue_block) (catch_block) (after_block)
  (anonymous_function) (stab_clause)
  (arguments) (list) (map) (tuple)
] @indent

["end" "}" "]" ")" "else" "rescue" "catch" "after"] @outdent

; While a block is being typed, before its `end`.
["do" "fn" "else" "rescue" "catch" "after"] @open
