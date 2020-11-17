from odoo import api, fields, models
from odoo.tools.translate import _
from datetime import date, datetime, timedelta
from odoo.http import request


class website(models.Model):
    _inherit = "website"

    def _get_default_header_content(self):
        return """
            <div class="s_rating row te_s_header_offer_text">
                <ul>
                    <li>Europaweite Lieferungen</li>
                    <li>
                        <section>|</section>
                    </li>
                    <li>Auf Wunsch mit Aufbau</li>
                    <li>
                        <section>|</section>
                    </li>
                    <li>Mengenrabatte auf Anfrage</li>
                </ul>
            </div>
            """

    def _get_default_footer_extra_links(self):
        return """
        <section>
            <div class="te_footer_inline_menu">
                <ul class="te_footer_inline_menu_t">
                    <section>
                        <li>
                            <a href="https://www.ketchup-mayo-senf.de/ueberuns">Über uns</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="https://www.ketchup-mayo-senf.de/kontakt">Kontakt</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="https://www.ketchup-mayo-senf.de/impressum">Impressum</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="https://www.ketchup-mayo-senf.de/datenschutz">Datenschutz</a>
                        </li>
                    </section>
                </ul>
            </div>
        </section>
        """

    def _get_default_footer_content(self):
        return """
            <p></p>
            <div class="row">
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/hilfe">Hilfe</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/gutscheine">Gutscheine</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/bestellstatus">Bestellstatus</a>
                            </li>
                        </section>
                    </ul>
                </div>
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/ueberuns">Über uns</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/jobs">Jobs</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/kontakt">Kontakt</a>
                            </li>
                        </section>
                    </ul>
                </div>
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/datenschutz">Datenschutz</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/impressum">Impressum</a>
                            </li>
                        </section>
                    </ul>
                </div>
            </div>
        """
    def _get_footer_style_3_content(self):
        return """
            <section>
                <div>
                    <h4 class="te_footer_menu_info">Informations</h4>
                </div>
            </section>
            <div class="row">
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/hilfe">Hilfe</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/gutscheine">Gutscheine</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/bestellstatus">Bestellstatus</a>
                            </li>
                        </section>
                    </ul>
                </div>
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/ueberuns">Über uns</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/jobs">Jobs</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/kontakt">Kontakt</a>
                            </li>
                        </section>
                    </ul>
                </div>
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/datenschutz">Datenschutz</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="https://www.ketchup-mayo-senf.de/impressum">Impressum</a>
                            </li>
                        </section>
                    </ul>
                </div>
            </div>
        """
    def _get_default_header_extra_links(self):
        return """
            <div class="te_header_static_menu">
                <ul>
                    <li>
                        <a href="https://www.ketchup-mayo-senf.de/">Startseite</a>
                    </li>
                    <li>
                        <a href="https://www.ketchup-mayo-senf.de/shop">Shop</a>
                    </li>
                    <li>
                        <a href="https://www.ketchup-mayo-senf.de/portfolio">Portfolio</a>
                    </li>
                    <li>
                        <a href="https://www.ketchup-mayo-senf.de/kundenprojekte">Kundenprojekte</a>
                    </li>
                    <li>
                        <a href="https://www.ketchup-mayo-senf.de/blog">Blog</a>
                    </li>
                    <li>
                        <a href="https://www.ketchup-mayo-senf.de/kontakt">Kontakt</a>
                    </li>
                </ul>
            </div>
        """

    def _get_default_header_extra_content(self):
        return """
            <div class="s_rating row te_s_header_offer_text">
                <ul>
                    <li><span>Email:</span>info@clauss-palacios.com</li>
                    <li>
                        <section>|</section>
                    </li>
                    <li>Fragen sie uns nach aktuellen Angeboten</li>
                </ul>
            </div>
        """
