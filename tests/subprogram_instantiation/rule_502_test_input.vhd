
package pkg is

  procedure my_proc is new my_generic_proc
    generic map (
      test => 2
    );

  function my_func is new my_generic_func
    generic map (
      test => 2
    );

  procedure my_proc is NEW my_generic_proc
    generic map (
      test => 2
    );

  function my_func is NEW my_generic_func
    generic map (
      test => 2
    );

  procedure my_proc is New my_generic_proc
    generic map (
      test => 2
    );

  function my_func is New my_generic_func
    generic map (
      test => 2
    );

end package;
