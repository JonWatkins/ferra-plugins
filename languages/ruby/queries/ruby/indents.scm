[
  (method) (singleton_method) (class) (singleton_class) (module)
  (if) (unless) (while) (until) (for) (case) (when) (begin) (else) (elsif)
  (do_block) (block) (hash) (array) (argument_list) (method_parameters)
] @indent

["end" "}" "]" ")" "else" "elsif" "when" "rescue" "ensure"] @outdent

; While a block is being typed, before its `end`.
["def" "class" "module" "if" "unless" "while" "until" "for" "case" "begin" "do"
 "when" "else" "elsif" "rescue" "ensure"] @open
