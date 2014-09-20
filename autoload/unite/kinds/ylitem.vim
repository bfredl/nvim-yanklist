let s:save_cpo = &cpo
set cpo&vim

function! unite#kinds#ylitem#define() "{{{
  return s:kind
endfunction"}}}

let s:kind = {
      \ 'name' : 'ylitem',
      \ 'default_action' : 'paste',
      \ 'action_table': {},
      \}

function! s:paste(candidate, pcmd, mode)
    let value = a:candidate.action__value
    if strlen(a:mode) > 0
        let value[1] = a:mode
    end
    call rpcrequest(g:yanklist_channel, "yanklist_choose", value)
    execute 'normal! '.a:pcmd

    " Open folds.
    normal! zv
endfunction


" Actions "{{{
let s:kind.action_table.paste = {
      \ 'description' : 'Paste word or text',
      \ }

function! s:kind.action_table.paste.func(candidate) "{{{
    call s:paste(a:candidate, 'p', '')
endfunction"}}}

let s:kind.action_table.ppaste = {
      \ 'description' : 'Paste word or text before',
      \ }

function! s:kind.action_table.ppaste.func(candidate) "{{{
    call s:paste(a:candidate, 'P', '')
endfunction"}}}

let s:kind.action_table.linepaste = {
      \ 'description' : 'Paste word or text linewise',
      \ }

function! s:kind.action_table.linepaste.func(candidate) "{{{
    call s:paste(a:candidate, 'p', 'V')
endfunction"}}}

let s:kind.action_table.plinepaste = {
      \ 'description' : 'Paste word or text linewise before',
      \ }

function! s:kind.action_table.plinepaste.func(candidate) "{{{
    call s:paste(a:candidate, 'P', 'V')
endfunction"}}}

let s:kind.action_table.charpaste = {
      \ 'description' : 'Paste word or text charwise',
      \ }

function! s:kind.action_table.charpaste.func(candidate) "{{{
    call s:paste(a:candidate, 'p', 'v')
endfunction"}}}

let s:kind.action_table.pcharpaste = {
      \ 'description' : 'Paste word or text charwise before',
      \ }

function! s:kind.action_table.pcharpaste.func(candidate) "{{{
    call s:paste(a:candidate, 'P', 'v')
endfunction"}}}
"}}}

let &cpo = s:save_cpo
unlet s:save_cpo


