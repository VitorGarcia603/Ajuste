document.addEventListener("DOMContentLoaded", () => {

  const toggleBtn = document.getElementById("themeToggle");
  const root      = document.documentElement;
  const prefKey   = "theme";
  const setTheme  = t => { root.dataset.bsTheme = t; localStorage.setItem(prefKey, t); };
  setTheme(localStorage.getItem(prefKey) || "light");
  toggleBtn?.addEventListener("click", () => {
    setTheme(root.dataset.bsTheme === "light" ? "dark" : "light");
    toggleBtn.querySelector("i").classList.toggle("bi-moon");
    toggleBtn.querySelector("i").classList.toggle("bi-sun");
  });

  const table = $('#tblEstoque').DataTable({
      serverSide: true,
      ajax: {
        url: "/estoque/data",
        data: d => {
          d.search = { value: $('#searchBox').val() };
          d.categoria = $('#catSelect').val();
        }
      },
      columns: [
        { data: "id" },
        { data: "nome" },
        { data: "categoria" },
        { data: "estoque" },
        { data: "custo" },
        {
          data: null,
          orderable: false,
          defaultContent:
            '<button class="btn btn-sm btn-outline-primary movimentar">Movimentar</button>'
        }
      ]
  });

  $('#searchBox, #catSelect').on('input change', () => table.ajax.reload());

  $('#tblEstoque').on('click', '.movimentar', function () {
    const data = table.row($(this).parents('tr')).data();
    $('#movProdId').val(data.id);
    $('#movForm')[0].reset();
    $('.div-custo').show();
    $('#movModal').modal('show');
  });

  $('select[name="tipo"]').on('change', function(){
    $('.div-custo').toggle(this.value === 'entrada');
  });

  $('#movForm').on('submit', function (e) {
    e.preventDefault();
    $.post('/estoque/movimentar', $(this).serialize())
      .done(() => {
        showToast("Movimentação concluída ✔️", "success");
        $('#movModal').modal('hide');
        table.ajax.reload(null,false);
      })
      .fail(() => showToast("Erro ao movimentar ❌", "danger"));
  });

  const toastEl = new bootstrap.Toast('#liveToast', { delay: 3000 });
  function showToast(msg, type){
    const body = document.querySelector('#liveToast .toast-body');
    body.textContent = msg;
    body.parentElement.className = \`toast align-items-center text-bg-\${type}\`;
    toastEl.show();
  }
});
