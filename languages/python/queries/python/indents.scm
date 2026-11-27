[
  (class_definition) (function_definition) (if_statement) (elif_clause)
  (else_clause) (for_statement) (while_statement) (try_statement)
  (except_clause) (finally_clause) (with_statement) (with_clause)
  (match_statement) (case_clause)
  (argument_list) (parameters) (list) (tuple) (dictionary) (set)
  (parenthesized_expression) (subscript) (list_comprehension)
  (dictionary_comprehension) (set_comprehension) (generator_expression)
  (import_from_statement) (type_parameter)
  (expression_statement) (return_statement) (raise_statement)
  (assert_statement) (delete_statement)
] @indent
[")" "]" "}"] @outdent
(elif_clause "elif" @outdent)
(else_clause "else" @outdent)
(except_clause "except" @outdent)
(finally_clause "finally" @outdent)
