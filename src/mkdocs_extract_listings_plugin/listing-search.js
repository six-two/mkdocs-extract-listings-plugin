// https://github.com/farzher/fuzzysort v2.0.4
((r,e)=>{"function"==typeof define&&define.amd?define([],e):"object"==typeof module&&module.exports?module.exports=e():r.fuzzysort=e()})(this,r=>{"use strict";var i,o,e,a,f=r=>{var e=v(r="string"!=typeof r?"":r);return{target:r,t:e.i,o:e.v,u:N,l:e.g,score:N,_:[0],obj:N}},t=r=>{r=(r="string"!=typeof r?"":r).trim();var e=v(r),a=[];if(e.p)for(var f,t=r.split(/\s+/),t=[...new Set(t)],n=0;n<t.length;n++)""!==t[n]&&(f=v(t[n]),a.push({v:f.v,i:t[n].toLowerCase(),p:!1}));return{v:e.v,g:e.g,p:e.p,i:e.i,h:a}},M=r=>{var e;return 999<r.length?f(r):(void 0===(e=n.get(r))&&(e=f(r),n.set(r,e)),e)},q=r=>{var e;return 999<r.length?t(r):(void 0===(e=s.get(r))&&(e=t(r),s.set(r,e)),e)},D=(r,e,a=!1)=>{if(!1===a&&r.p)return j(r,e);for(var a=r.i,f=r.v,t=f[0],n=e.o,i=f.length,o=n.length,v=0,s=0,u=0;;){if(t===n[s]){if(C[u++]=s,++v===i)break;t=f[v]}if(o<=++s)return N}var v=0,l=!1,g=0,d=e.u,c=(d===N&&(d=e.u=k(e.target)),s=0===C[0]?0:d[C[0]-1],0);if(s!==o)for(;;)if(o<=s){if(v<=0)break;if(200<++c)break;--v;s=d[L[--g]]}else if(f[v]===n[s]){if(L[g++]=s,++v===i){l=!0;break}++s}else s=d[s];var w=e.t.indexOf(a,C[0]),r=~w;if(r&&!l)for(var _=0;_<u;++_)C[_]=w+_;a=!1;r&&(a=e.u[w-1]===w);p=l?(b=L,g):(b=C,u);for(var b,p,x=0,h=0,_=1;_<i;++_)b[_]-b[_-1]!=1&&(x-=b[_],++h);if(x-=(12+(b[i-1]-b[0]-(i-1)))*h,0!==b[0]&&(x-=b[0]*b[0]*.2),l){for(var y=1,_=d[0];_<o;_=d[_])++y;24<y&&(x*=10*(y-24))}else x*=1e3;r&&(x/=1+i*i*1),a&&(x/=1+i*i*1),e.score=x-=o-i;for(_=0;_<p;++_)e._[_]=b[_];return e._.j=p,e},j=(r,e)=>{for(var a=new Set,f=0,t=N,n=0,i=r.h,o=0;o<i.length;++o){var v=i[o];if((t=D(v,e))===N)return N;f+=t.score,t._[0]<n&&(f-=n-t._[0]);for(var n=t._[0],s=0;s<t._.j;++s)a.add(t._[s])}r=D(r,e,!0);if(r!==N&&r.score>f)return r;t.score=f;var u,o=0;for(u of a)t._[o++]=u;return t._.j=o,t},v=r=>{for(var e=r.length,a=r.toLowerCase(),f=[],t=0,n=!1,i=0;i<e;++i){var o=f[i]=a.charCodeAt(i);32===o?n=!0:t|=1<<(97<=o&&o<=122?o-97:48<=o&&o<=57?26:o<=127?30:31)}return{v:f,g:t,p:n,i:a}},k=r=>{for(var e=r.length,a=(r=>{for(var e=r.length,a=[],f=0,t=!1,n=!1,i=0;i<e;++i){var o=r.charCodeAt(i),v=65<=o&&o<=90,o=v||97<=o&&o<=122||48<=o&&o<=57,s=v&&!t||!n||!o,t=v,n=o;s&&(a[f++]=i)}return a})(r),f=[],t=a[0],n=0,i=0;i<e;++i)i<t?f[i]=t:(t=a[++n],f[i]=void 0===t?e:t);return f},n=new Map,s=new Map,C=[],L=[],E=r=>{for(var e=J,a=r.length,f=0;f<a;++f){var t=r[f];t!==N&&e<(t=t.score)&&(e=t)}return e===J?N:e},F=(r,e)=>{var a=r[e];if(void 0!==a)return a;for(var f=e,t=(f=Array.isArray(e)?f:e.split(".")).length,n=-1;r&&++n<t;)r=r[f[n]];return r},G=r=>"object"==typeof r,H=1/0,J=-H,K=[],N=null,O=(i=[],o=K.total=0,a=r=>{for(var e=i[t=0],a=1;a<o;){var f=a+1,t=a;f<o&&i[f].score<i[a].score&&(t=f),i[t-1>>1]=i[t],a=1+(t<<1)}for(var n=t-1>>1;0<t&&e.score<i[n].score;n=(t=n)-1>>1)i[t]=i[n];i[t]=e},(e={}).add=r=>{var e=o;i[o++]=r;for(var a=e-1>>1;0<e&&r.score<i[a].score;a=(e=a)-1>>1)i[e]=i[a];i[e]=r},e.k=r=>{var e;if(0!==o)return e=i[0],i[0]=i[--o],a(),e},e.C=r=>{if(0!==o)return i[0]},e.L=r=>{i[0]=r,a()},e);return{single:(r,e)=>{var a;return"farzher"==r?{target:"farzher was here (^-^*)/",score:0,_:[0]}:!r||!e||(r=q(r),G(e)||(e=M(e)),((a=r.g)&e.l)!==a)?N:D(r,e)},go:(r,e,a)=>{if("farzher"==r)return[{target:"farzher was here (^-^*)/",score:0,_:[0],obj:e?e[0]:N}];if(!r)if(a&&a.all){var f=e;var t=a;var n=[],i=(n.total=f.length,t&&t.limit||H);if(t&&t.key)for(var o=0;o<f.length;o++){var v=f[o];var s=F(v,t.key);if(!s)continue;if(!G(s))s=M(s);s.score=J;s._.j=0;var u=s;u={target:u.target,t:"",o:N,u:N,l:0,score:s.score,_:N,obj:v};n.push(u);if(n.length>=i)return n}else if(t&&t.keys)for(o=0;o<f.length;o++){v=f[o];var l=new Array(t.keys.length);for(var g=t.keys.length-1;g>=0;--g){s=F(v,t.keys[g]);if(!s){l[g]=N;continue}if(!G(s))s=M(s);s.score=J;s._.j=0;l[g]=s}l.obj=v;l.score=J;n.push(l);if(n.length>=i)return n}else for(o=0;o<f.length;o++){s=f[o];if(!s)continue;if(!G(s))s=M(s);s.score=J;s._.j=0;n.push(s);if(n.length>=i)return n}return n;return}else return K;var d=q(r),c=d.g,w=(d.p,a&&a.threshold||J),_=a&&a.limit||H,b=0,p=0,x=e.length;if(a&&a.key)for(var h=a.key,y=0;y<x;++y){var j=e[y];!(m=F(j,h))||(c&(m=G(m)?m:M(m)).l)!==c||(B=D(d,m))===N||B.score<w||(B={target:B.target,t:"",o:N,u:N,l:0,score:B.score,_:B._,obj:j},b<_?(O.add(B),++b):(++p,B.score>O.C().score&&O.L(B)))}else if(a&&a.keys)for(var k=a.scoreFn||E,C=a.keys,L=C.length,y=0;y<x;++y){for(var j=e[y],S=new Array(L),z=0;z<L;++z){h=C[z];(m=F(j,h))?(c&(m=G(m)?m:M(m)).l)!==c?S[z]=N:S[z]=D(d,m):S[z]=N}S.obj=j;var A=k(S);A===N||A<w||(S.score=A,b<_?(O.add(S),++b):(++p,A>O.C().score&&O.L(S)))}else for(var m,B,y=0;y<x;++y)!(m=e[y])||(c&(m=G(m)?m:M(m)).l)!==c||(B=D(d,m))===N||B.score<w||(b<_?(O.add(B),++b):(++p,B.score>O.C().score&&O.L(B)));if(0===b)return K;for(var I=new Array(b),y=b-1;0<=y;--y)I[y]=O.k();return I.total=b+p,I},highlight:(r,e,a)=>{if("function"==typeof e){var f=e;if((l=r)===N)return N;for(var t=l.target,n=t.length,i=(i=l._).slice(0,i.j).sort((r,e)=>r-e),o="",v=0,s=0,u=!1,l=[],g=0;g<n;++g){var d=t[g];if(i[s]===g){if(++s,u||(u=!0,l.push(o),o=""),s===i.length){o+=d,l.push(f(o,v++)),o="",l.push(t.substr(g+1));break}}else u&&(u=!1,l.push(f(o,v++)),o="");o+=d}return l}if(r===N)return N;void 0===e&&(e="<b>"),void 0===a&&(a="</b>");for(var c="",w=0,_=!1,b=r.target,p=b.length,x=(x=r._).slice(0,x.j).sort((r,e)=>r-e),h=0;h<p;++h){var y=b[h];if(x[w]===h){if(_||(_=!0,c+=e),++w===x.length){c+=y+a+b.substr(h+1);break}}else _&&(_=!1,c+=a);c+=y}return c},prepare:f,indexes:r=>r._.slice(0,r._.j).sort((r,e)=>r-e),cleanup:()=>{n.clear(),s.clear(),C=[],L=[]}}});

// My code

// How many results to show as a preview while changing the search query.
// This limits load required to parse entries, etc and should result in the user getting some quick feedback on his/her search
(() => {
PREVIEW_RESULTS = 15;
DEFAULT_SEARCH_MODE=null;
// START: These values may be overwritten when the file is copied by the plugin
STYLE=``;
OFFLINE_JSON_DATA=null;
// END

// Convert relative to absolute URL
const normalizeUrl = (url) => {
    return new URL(url, location.href).pathname;
};

const createRegexFromBlob = (string) => {
    // From: https://stackoverflow.com/questions/3561493/is-there-a-regexp-escape-function-in-javascript but removed * and ?
    string = string.replace(/[/\-\\^$+.()|[\]{}]/g, '\\$&');
    // handle blob characters
    // .* does not match line breaks, so we need to use [^] for "every character including line break" (everything except: nothing)
    string = string.replaceAll("?", ".").replaceAll("*", "[^]*"); 

    return RegExp(string);
}

const parent = document.getElementById("listing-extract-search");
if (parent) {
    const search_mode = parent.getAttribute("data-searchmode") || DEFAULT_SEARCH_MODE;

    const add_link = (parent_element, href, title, className) => {
        const element = document.createElement("a");
        element.href = href;
        element.innerText = title;
        if (className) {
            element.classList.add(className);
        }
        if (parent_element) {
            parent_element.append(element);
        }
        return element;
    };

    const add_div = (parent_element, className, ...children) => {
        const element = document.createElement("div");
        element.classList.add(className);
        if (children) {
            element.append(...children);
        }
        if (parent_element) {
            parent_element.append(element);
        }
        return element;
    }

    const search_input = document.createElement("input");
    search_input.classList.add("md-input", "md-input--stretch");
    search_input.placeholder = "Search listings by typing here";
    search_input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            search(e.target.value, false);
        }
    });
    const refresh_search_results = () => search(search_input.value, true);
    search_input.addEventListener("input", refresh_search_results);

    const search_count_div = document.createElement("div");
    search_count_div.classList.add("search-count");
    search_count_div.innerText = "Loading listing data...";
    
    const search_type = document.createElement("select");
    const search_type_list = [];
    const add_search_type = (value, title) => {
        search_type_list.push(value);
        const entry = document.createElement("option");
        entry.value = value;
        entry.innerText = title;
        search_type.append(entry);
    }

    add_search_type("substr", "Exact match");
    add_search_type("substr-i", "Exact match (case insensitive)");
    add_search_type("words", "Contains words");
    add_search_type("words-i", "Contains words (case insensitive)");
    add_search_type("glob", "Matches blobs ('*'=any sequence of characters, '?'=any character)");
    add_search_type("glob-i", "Matches blobs (case insensitive)");
    add_search_type("fuzzy", "Fuzzy search (always case insensitive)");

    default_index = search_type_list.indexOf(search_mode);
    if (default_index != -1) {
        search_type.selectedIndex = default_index;
    } else {
        console.warn(`The search order type '${search_mode}' is unknown. Valid values are ${search_type_list}`)
    }
    
    const search_language = document.createElement("select");
    const add_search_language = (name) => {
        const entry = document.createElement("option");
        entry.value = name;
        entry.innerText = name;
        search_language.append(entry);
    }
        
    add_search_language("any") // default option

    search_type.title = "The search algorithm to use";
    search_language.title = "Only show snippets in this language";

    search_type.addEventListener("change", refresh_search_results);
    search_language.addEventListener("change", refresh_search_results);
        
    const search_input_line = add_div(null, "search-input-line", search_input, search_type, search_language);
    add_div(parent, "search-inputs", search_input_line, search_count_div);
    const search_output = add_div(parent, "search-output");
    console.debug("Attached search to ", parent);


    const set_search_results = (results) => {
        for (const result of results) {
            const header = add_link(null, result.page_url, result.page_name, "heading");
            const page_url = add_link(null, result.page_url, result.page_url, "url");

            const div = document.createElement("div");
            div.classList.add("listing");
            div.innerHTML = result.html;
            
            add_div(search_output, "search-result", header, page_url, div);
        }
    }

    const get_words = (text) => {
        return text.match(/\b\w+\b/g) || [];
    }

    const internal_search = (query, search_mode, filter_language) => {
        // Handle the differences between case sensitive and insensitive search
        let listings_list;
        if (search_mode.endsWith("-i")) {
            // Search mode without the -i
            search_mode = search_mode.slice(0, -2);
            // Use the lowercase versions of the query and the search data
            query = query.toLowerCase();
            listings_list = window.extract_listings_lowercase;
        } else {
            listings_list = window.extract_listings_case_sensitive;
        }


        // Handle the language filter
        if (filter_language != "any") {
            // We need to pre-filter the listings by the programming language
            listings_list = listings_list.filter(x => x.language == filter_language);
        }


        // Handle the different search modes
        if (search_mode == "substr") {
            return listings_list.filter(x => x.text.includes(query));
        } else if (search_mode == "words") {
            const query_words = get_words(query);
            if (query_words) {
                return listings_list.filter(x => {
                    const text_words = get_words(x.text);
                    return query_words.every(w => text_words.includes(w));
                });
            } else {
                // Empty search queries return all listings for all other search types, so we should do the same here
                return listings_list;
            }
        } else if (search_mode == "glob") {
            query_regex = createRegexFromBlob(query);
            console.debug("Using regex:", query_regex);
            return listings_list.filter(x => query_regex.test(x.text));
        } else if (search_mode == "fuzzy") {
            return fuzzysort.go(query, listings_list, {
                "key": "text",
                "all": true, // show all results when the query is empty
                threshold: -10000, // prevent terrible results
            }).map(x => x.obj);
        } else {
            alert(`Unknown search type: ${search_mode}`);
            return [];
        }
    }


    const search = (query, preview) => {
        const search_mode = search_type.value;
        const filter_language = search_language.value;
        console.debug(`Searching for '${query}' with method ${search_mode} and language ${filter_language}`);
        const results = internal_search(query, search_mode, filter_language);

        search_output.innerHTML = "";//remove children

        if (preview && results.length > PREVIEW_RESULTS) {
            search_count_div.innerHTML = `Found ${results.length} results. Preview is limited to ${PREVIEW_RESULTS}, press <code>Enter</code> to show them all`;
            set_search_results(results.slice(0, PREVIEW_RESULTS));
        } else {
            search_count_div.innerText = `Found ${results.length} result(s)`;
            set_search_results(results);
        }        
    }

    if (STYLE) {
        const style = document.createElement("style");
        style.innerHTML = STYLE;
        document.body.append(style);
    }

    const on_json_loaded = (json) => {
        // Publicly accessible for easier debugging
        // Remap the URLs based on the location of this script (which is in the same directory as the JSON file)
        window.extract_listings_case_sensitive = json.map(x => ({...x, page_url: normalizeUrl(x.page_url)}));
        // @TODO: maybe only cache this if an cae-insensitive mode is selected?
        window.extract_listings_lowercase = window.extract_listings_case_sensitive.map(x => ({...x, text: x.text.toLowerCase()}));

        let language_list = json.map(x => x.language);
        // remove duplicates and sort alphabetically
        language_list = [...new Set(language_list)].sort();
        // register all languages for the dropdown menu
        language_list.forEach(language => add_search_language(language));

        if (language_list.length < 2) {
            console.debug("It does not make sense to show the selector, since there is only one choice -> hiding language dropdown");
            search_language.style.display = "none";
        }

        // As soon as all data is loaded, search for the current value
        // Use preview to prevent a self-DOS when there are many listings and the query is empty
        refresh_search_results();
    };

    if (OFFLINE_JSON_DATA != null) {
        on_json_loaded(OFFLINE_JSON_DATA);
    } else {
        fetch(document.currentScript.src + ".json")
            .then(req => req.json())
            .then(on_json_loaded);
    }
} else {
    console.warn("Could not find any element with id 'listing-extract-search'")
}
})();
