function! unite#sources#yanklist#define() "{{{
  return s:source
endfunction"}}}

let s:source = {
      \ 'name' : 'yanklist',
      \ 'description' : 'yank history',
      \ 'action_table' : {},
      \ 'default_kind' : 'ylitem',
      \}

function! s:source.gather_candidates(args, context) "{{{
    "FIXME: probably a better way
    return rpcrequest(g:yanklist_channel, "yanklist_candidates")

endfunction"}}}
