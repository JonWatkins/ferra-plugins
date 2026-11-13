[
  (function_declaration)
  (function_definition)
  (if_statement)
  (elseif_statement)
  (else_statement)
  (for_statement)
  (while_statement)
  (repeat_statement)
  (do_statement)
  (table_constructor)
  (arguments)
  (parameters)
] @indent

["end" "until" "else" "elseif" "}" ")"] @outdent

; While a block is being typed (its `end` not there yet), these open it.
["function" "then" "do" "repeat" "else" "elseif"] @open
