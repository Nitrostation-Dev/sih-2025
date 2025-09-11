{
	description = "Flake for Python Development";

	outputs = { self, nixpkgs, nixvim, ... }:
	let
		system = "x86_64-linux";
		pkgs = import nixpkgs { inherit system; };

	in {

		packages.${system}.nixvim = nixvim.legacyPackages.${system}.makeNixvim {
			config = {
				colorschemes.catppuccin.enable = true;

				clipboard.register = "unnamedplus";
				opts = {
					number = true;
					relativenumber = true;
					mouse = "a";

					tabstop = 4;
					shiftwidth = 4;

					showmode = true;

					breakindent = true;

					undofile = true;

					ignorecase = true;
					smartcase = true;

					signcolumn = "yes";

					updatetime = 250;
					timeoutlen = 300;

					splitright = true;

					splitbelow = true;

					inccommand = "split";

					cursorline = true;
					scrolloff = 10;
					confirm = true;
				};
				globals = {
					mapleader = " ";
					maplocalleader = " ";
				};

				extraConfigLua = ''
vim.diagnostic.config {
	severity_sort = true,
	float = { border = 'rounded', source = 'if_many' },
	underline = { severity = vim.diagnostic.severity.ERROR },
	signs = vim.g.have_nerd_font and {
		text = {
			[vim.diagnostic.severity.ERROR] = '󰅚 ',
			[vim.diagnostic.severity.WARN] = '󰀪 ',
			[vim.diagnostic.severity.INFO] = '󰋽 ',
			[vim.diagnostic.severity.HINT] = '󰌶 ',
		} or {},
		virtual_text = {
			source = 'if_many',
			spacing = 4,
			format = function(diagnostic)
				local diagnostic_message = {
					[vim.diagnostic.severity.ERROR] = diagnostic.message,
					[vim.diagnostic.severity.WARN] = diagnostic.message,
					[vim.diagnostic.severity.INFO] = diagnostic.message,
					[vim.diagnostic.severity.HINT] = diagnostic.message,
				}
				return diagnostic_message[diagnostic.severity]
			end,
		},
	},
}
				'';

				lsp.inlayHints.enable = true;

				plugins = {
					lsp = {
						enable = true;
						servers = {
							pyright.enable = true;
							jsonls.enable = true;
						};
					};

					cmp = {
						enable = true;
						settings = {
							sources = [
								{ name = "lazydev"; groupIndex = 0; }
								{ name = "nvim_lsp"; }
								{ name = "luasnip"; }
								{ name = "path"; }
								{ name = "nvim_lsp_signature_help"; }
							];

							snippet = {
								expand = "function(args) require('luasnip').lsp_expand(args.body) end";
							};

							mapping = {
								"<Tab>" = "cmp.mapping.select_next_item()";
								"<S-Tab>" = "cmp.mapping.select_prev_item()";
								"<C-f>" = "cmp.mapping.scroll_docs(-4)";
								"<C-s>" = "cmp.mapping.scroll_docs(4)";
								"<C-n>" = "cmp.mapping.confirm { select = true }";
								"<C-k>" = "
									cmp.mapping(
										function()
											local luasnip = require('luasnip')
											if luasnip.expand_or_locally_jumpable() then
												luasnip.expand_or_jump()
											end
										end,
										{\"i\", \"s\"}
									)
								";
								"<C-h>" = "
									cmp.mapping(
										function()
											local luasnip = require('luasnip')
											if luasnip.locally_jumpable(-1) then
												luasnip.jump(-1)
											end
										end,
										{\"i\", \"s\"}
									)
								";
							};
						};
					};
					cmp_luasnip.enable = true;
					cmp-nvim-lsp.enable = true;
					cmp-path.enable = true;
					cmp-buffer.enable = true;
					cmp-npm.enable = true;

					treesitter = {
						enable = true;
						settings = {
							auto_install = true;
							ensure_installed = [
								"git_config"
								"git_rebase"
								"gitattributes"
								"gitcommit"
								"gitignore"

								"python"
							];
						};
					};

					luasnip = {
						enable = true;
					};

					conform-nvim = {
						enable = true;
						settings = {
							formatters_by_ft = {
								"*" = [ "codespell" ];
								"_" = [ "trim_whitespace" ];

								"python" = [ "black" ];
							};
						};
					};

					indent-blankline = {
						enable = true;
						settings = {
							exclude = {
								buftypes = [
									"terminal"
									"quickfix"
								];

								filetypes = [
									  ""
									  "checkhealth"
									  "help"
									  "lspinfo"
									  "packer"
									  "TelescopePrompt"
									  "TelescopeResults"
									  "yaml"
								];
							};
							indent = {
								char = "╎";
							};
							scope = {
								show_end = false;
								show_exact_scope = true;
								show_start = false;
							};
						};
					};

					mini = {
						enable = true;
						modules = {
							basics = {
								options = {
									basic = true;
									extra_ui = false;
									win_borders = "default";
								};

								mappings = {
									basic = true;
									windows = true;
									move_with_alt = true;
								};

								autocommands = {
									basic = true;
								};

								silent = false;
							};

							files = {
								mappings = {
									close       = "q";
									go_in       = "<Right>";
									go_out      = "<Left>";
									mark_goto   = "\"";
									mark_set    = "m";
									reset       = "<BS>";
									reveal_cwd  = "@";
									show_help   = "g?";
									synchronize = "=";
									trim_left   = "<";
									trim_right  = ">";
								};
							};

							pairs = {
								modes = {
									insert = true;
									command = false;
									terminal = false;
								};
							};

							comment = {
								mappings = {
									comment = "gc";
									comment_line = "gcc";
									comment_visual = "gc";
									text_object = "gc";
								};
							};

							notify = {
								content = {
									format = null;
									sort = null;
								};

								lsp_progress = {
									enable = true;
									level = "INFO";
									duration_last = 1000;
								};

								window = {
									config = {};
									max_width_share = 0.382;
									winblend = 25;
								};
							};

							clue = {
								triggers = [
									{ mode = "n"; keys = "<Leader>"; }
									{ mode = "x"; keys = "<Leader>"; }

									{ mode = "i"; keys = "<C-x>"; }

									{ mode = "n"; keys = "g"; }
									{ mode = "x"; keys = "g"; }

									{ mode = "n"; keys = "\""; }
									{ mode = "n"; keys = "`"; }
									{ mode = "x"; keys = "\""; }
									{ mode = "x"; keys = "`"; }

									{ mode = "n"; keys = "\""; }
									{ mode = "x"; keys = "\""; }
									{ mode = "i"; keys = "<C-r>"; }
									{ mode = "c"; keys = "<C-r>"; }

									{ mode = "n"; keys = "<C-w>"; }

									{ mode = "n"; keys = "z"; }
									{ mode = "x"; keys = "z"; }
								];

								window = {
									delay = 50;

									scroll_down = "<C-d>";
									scoll_up = "<C-u>";
								};
							};
						};
					};

					telescope = {
						enable = true;
						extensions = {
							ui-select.enable = true;
							fzf-native.enable = true;
						};
					};

					gitsigns = {
						enable = true;
						settings = {
							signs = {
								add = { text = "+"; };
								change = { text = "~"; };
								delete = { text = "_"; };
								topdelete = { text = "‾"; };
								changedelete = { text = "~"; };
							};
						};
					};

					lualine = {
						enable = true;
					};

					barbar = {
						enable = true;
						settings = {
							animation = false;
						};
					};

					toggleterm = {
						enable = true;
						settings = {
							direction = "float";
						};
					};

					indent-o-matic = {
						enable = true;
						settings = {
							max_lines = 2048;
							standard_widths = [ 2 4 8 ];
						};
					};

					# sleuth.enable = true;
					ccc.enable = true;
					web-devicons.enable = true;
				};

				keymaps = [
					{ mode = "n"; key = "<Esc>"; action = "<cmd>nohlsearch<CR>"; }
					{ mode = "n"; key = "<leader>pv"; action = "<cmd>Ex<CR>"; options.desc = "Open Neovim Explorer"; }
					{ mode = "n"; key = "<leader>e"; action = "<cmd>lua MiniFiles.open()<CR>"; options.desc = "Open Mini Files Explorer"; }

					{ mode = "n"; key = "<leader>sh"; action = ":Telescope help_tags<CR>"; options.desc = "[S]earch [H]elp"; }
					{ mode = "n"; key = "<leader>sk"; action = ":Telescope keymaps<CR>"; options.desc = "[S]earch [K]eymaps"; }
					{ mode = "n"; key = "<leader>sf"; action = ":Telescope find_files<CR>"; options.desc = "[S]earch [F]iles"; }
					{ mode = "n"; key = "<leader>ss"; action = ":Telescope builtin<CR>"; options.desc = "[S]earch [S]elect Telescope"; }
					{ mode = "n"; key = "<leader>sw"; action = ":Telescope grep_string<CR>"; options.desc = "[S]earch current [W]ord"; }
					{ mode = "n"; key = "<leader>sg"; action = ":Telescope live_grep<CR>"; options.desc = "[S]earch by [G]rep"; }
					{ mode = "n"; key = "<leader>sd"; action = ":Telescope diagnostics<CR>"; options.desc = "[S]earch [D]iagnostics"; }
					{ mode = "n"; key = "<leader>sr"; action = ":Telescope resume<CR>"; options.desc = "[S]earch [R]esume"; }
					{ mode = "n"; key = "<leader>s."; action = ":Telescope oldfiles<CR>"; options.desc = "[S]earch Recent Files (\".\" for repeat)"; }
					{ mode = "n"; key = "<leader><leader>"; action = ":Telescope buffers<CR>"; options.desc = "[ ] Find existing buffers"; }
					{ mode = "n"; key = "<leader>/";
						action = "lua require('telescope.builtin').current_buffer_fuzzy_find(require('telescope.themes').get_dropdown { winblend = 10, previewer = false })";
						options.desc = "[/] Fuzzily search in current buffer";
					}
					{ mode = "n"; key = "<leader>s/";
						action = "lua require('telescope.builtin').live_grep { grep_open_files = true, prompt_title = 'Live Grep in Open Files' }";
						options.desc = "[S]earch [/] in Open Files";
					}
					{ mode = "n"; key = "<leader>sn";
						action = "lua require('telescope.builtin').find_files { cwd = vim.fn.stdpath 'config' }";
						options.desc = "[S]earch [N]eovim files";
					}

					{ mode = "n"; key = "gd"; action = "<cmd>Telescope lsp_definitions<CR>"; options.desc = "[G]oto [D]definition"; }
					{ mode = "n"; key = "gr"; action = "<cmd>Telescope lsp_references<CR>"; options.desc = "[G]oto [R]eferences"; }
					{ mode = "n"; key = "gI"; action = "<cmd>Telescope lsp_implementations<CR>"; options.desc = "[G]oto [I]mplementation"; }
					{ mode = "n"; key = "<leader>D"; action = "<cmd>Telescope lsp_type_definitions<CR>"; options.desc = "Type [D]definition"; }
					{ mode = "n"; key = "<leader>ds"; action = "<cmd>Telescope lsp_document_symbols<CR>"; options.desc = "[D]ocument [S]symbols"; }
					{ mode = "n"; key = "<leader>ws"; action = "<cmd>Telescope lsp_dynamic_workspace_symbols<CR>"; options.desc = "[W]orkspace [S]symbols"; }
					{ mode = "n"; key = "<leader>rn"; action = "<cmd>lua vim.lsp.buf.rename()<CR>"; options.desc = "[R]e[n]ame"; }
					{ mode = "n"; key = "<leader>ca"; action = "<cmd>lua vim.lsp.buf.code_action()<CR>"; options.desc = "[C]ode [A]ction"; }
					{ mode = "n"; key = "gD"; action = "<cmd>lua vim.lsp.buf.declaration()<CR>"; options.desc = "[G]oto [D]eclaration"; }

					{ mode = "n"; key = "<leader>f"; action = "<cmd>lua require('conform').format { async = true, lsp_format = 'fallback' }<CR>";  options.desc = "[F]ormat Buffer"; }

					{ mode = "n"; key = "<C-`>"; action = "<cmd>ToggleTerm<CR>";  options.desc = "Toggle Terminal"; }

					{ mode = "n"; key = "<C-2>"; action = "<cmd>BufferNext<CR>"; options.desc = "Cycle to next buffer"; }
					{ mode = "n"; key = "<C-1>"; action = "<cmd>BufferPrevious<CR>"; options.desc = "Cycle to previous buffer"; }
					{ mode = "n"; key = "<C-3>"; action = "<cmd>BufferClose<CR>"; options.desc = "Close current active buffer"; }
				];
			};
		};

		devShells.${system}.default = pkgs.mkShell {
			nativeBuildInputs = [
				pkgs.git
				pkgs.black

				(pkgs.python3.withPackages (python-pkgs: [
					python-pkgs.tabulate
				]))
			];

			buildInputs = [
				self.packages.${system}.nixvim
				(pkgs.python3.withPackages (python-pkgs: [
					python-pkgs.tabulate
				]))
			];
		};
	};

	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
		nixvim.url = "github:nix-community/nixvim";
	};
}
