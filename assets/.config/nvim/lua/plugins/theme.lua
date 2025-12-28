return {
  -- 1. Plugin Pywal
  {
    "AlphaTechnolog/pywal.nvim",
    name = "pywal",
    lazy = false, -- Carrega imediatamente
    priority = 1000, -- Garante que carrega antes de outros plugins de UI
    config = function()
      local pywal = require("pywal")
      pywal.setup()

      -- Aplica o tema
      vim.cmd("colorscheme pywal")
    end,
  },

  -- 2. Ajuste da Barra de Status (Lualine)
  {
    "nvim-lualine/lualine.nvim",
    opts = function(_, opts)
      opts.options.theme = "pywal"
    end,
  },

  -- 3. Força o LazyVim a não carregar o Tokyonight automaticamente
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "pywal",
    },
  },
}
