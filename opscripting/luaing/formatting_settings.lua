local StrFmtSettings = {}

function StrFmtSettings:new()
  --[[
  A base class that hold configuration settings for string formatting used
  by stringify() and table2string()
  ]]

  -- these are the default values
  local attrs = {
    ["display_time"] = true,
    ["display_context"] = true,
    ["blocks_duplicate"] = true,
    -- how much decimals should be kept for floating point numbers
    ["numbers"] = {
      ["round"] = 3
    },
    -- nil by default cause the table2string already have some defaults
    ["tables"] = {
      -- how much whitespaces is considered an indent
      ["indent"] = 4,
      -- max table size before displaying it as oneline to avoid flooding
      ["length_max"] = 50,
      -- true to display the table on multiples lines with indents
      ["linebreaks"] = true,
      ["display_indexes"] = false,
      ["display_functions"] = true
    },
    ["strings"] = {
      ["display_quotes"] = false
    }
  }

  function attrs:set_display_time(enable)
    -- enable(bool): true to display the current time as h:m:s
    self.display_time = enable
  end

  function attrs:set_display_context(enable)
    -- enable(bool): true to display Logger.ctx
    self.display_context = enable
  end

  function attrs:set_blocks_duplicate(enable)
    -- enable(bool): true to enable blocking of repeated messages
    self.blocks_duplicate = enable
  end

  function attrs:set_num_round(round_value)
    -- round_value(int):
    self.numbers.round = round_value
  end

  function attrs:set_str_display_quotes(display_value)
    -- display_value(bool):
    self.strings.display_quotes = display_value
  end

  function attrs:set_tbl_display_indexes(display_value)
    -- display_value(bool):
    self.tables.display_indexes = display_value
  end

  function attrs:set_tbl_linebreaks(display_value)
    -- display_value(bool):
    self.tables.linebreaks = display_value
  end

  function attrs:set_tbl_length_max(length_max)
    -- length_max(int):
    self.tables.length_max = length_max
  end

  function attrs:set_tbl_indent(indent)
    -- indent(int):
    self.tables.indent = indent
  end

  function attrs:set_tbl_display_functions(display_value)
    -- display_value(bool):
    self.tables.display_functions = display_value
  end

  return attrs

end

return StrFmtSettings